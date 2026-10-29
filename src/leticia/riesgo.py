"""Índices de vulnerabilidad, clases de amenaza y riesgo, daño por inundación y pérdida anual esperada."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import parametros

CLASES = ["Muy baja", "Baja", "Media", "Alta", "Muy alta"]
COLORES_CLASES = ["#1a9850", "#91cf60", "#fee08b", "#fc8d59", "#d73027"]


def normalizar(s: pd.Series, invertir: bool = False) -> pd.Series:
    """Rango percentil (0–1): robusto a valores extremos y comparable entre variables."""
    r = s.rank(pct=True)
    return 1 - r if invertir else r


def clasificar(s: pd.Series, cortes=(0.2, 0.4, 0.6, 0.8), etiquetas=None) -> pd.Series:
    """Cinco clases a partir de un índice 0–1."""
    etiquetas = etiquetas or CLASES
    return pd.cut(s, bins=[-np.inf, *cortes, np.inf], labels=etiquetas)


def indice_vulnerabilidad(m: pd.DataFrame, columnas: dict[str, tuple[str, bool]] | None = None) -> pd.Series:
    """Índice ponderado de vulnerabilidad/exposición de la malla (pesos en `parametros.yaml`).

    `columnas` asocia cada peso a (columna, invertir). Las celdas sin edificaciones quedan en NaN.
    """
    pesos = parametros()["vulnerabilidad"]["pesos"]
    columnas = columnas or {
        "densidad_edificaciones": ("densidad_construida", False),
        "poblacion": ("poblacion", False),
        "proximidad_rio": ("dist_rio_m", True),
        "baja_vegetacion": ("ndvi", True),
    }
    total = pd.Series(0.0, index=m.index)
    usados = 0.0
    for clave, (col, inv) in columnas.items():
        if col in m and m[col].notna().any():
            total += pesos[clave] * normalizar(m[col], inv).fillna(0)
            usados += pesos[clave]
    idx = total / usados
    return idx.where(m.get("n_edif", pd.Series(1, index=m.index)) > 0)


def matriz_riesgo(amenaza: pd.Series, vulnerabilidad: pd.Series) -> pd.Series:
    """Combina clases de amenaza y vulnerabilidad (1–5) con la matriz habitual: riesgo = ⌈(a·v)/5⌉."""
    a = pd.Series(pd.Categorical(amenaza, categories=CLASES).codes + 1, index=amenaza.index).replace(0, np.nan)
    v = pd.Series(pd.Categorical(vulnerabilidad, categories=CLASES).codes + 1, index=vulnerabilidad.index).replace(0, np.nan)
    r = np.ceil(a * v / 5).clip(1, 5)
    return pd.Series(pd.Categorical.from_codes((r - 1).fillna(-1).astype(int), categories=CLASES), index=amenaza.index)


def fraccion_danio(profundidad_m) -> np.ndarray:
    """Fracción de daño de vivienda según la curva profundidad–daño de `parametros.yaml` (Huizinga et al. 2017)."""
    c = parametros()["inundacion"]["curva_danio"]
    return np.interp(np.asarray(profundidad_m, dtype=float), c["profundidad_m"], c["fraccion"], left=0, right=1)


def perdida_anual_esperada(perdidas: pd.Series) -> float:
    """Pérdida anual esperada integrando pérdida vs. probabilidad anual de excedencia (regla del trapecio).

    `perdidas` tiene como índice el periodo de retorno (años). Se supone pérdida nula para T < min(T) / 2.
    """
    s = perdidas.sort_index()
    p = 1 / s.index.to_numpy(dtype=float)
    v = s.to_numpy(dtype=float)
    p = np.append(p, min(1.0, 2 * p[0]))
    v = np.append(v, 0.0)
    orden = np.argsort(p)
    return float(np.trapezoid(v[orden], p[orden]))


def impacto_climada(lon, lat, valores, profundidades: dict[int, np.ndarray], curva: dict,
                    elevaciones_m: list[float] | None = None, region: np.ndarray | None = None) -> dict:
    """Pérdida anual esperada por inundación con CLIMADA (Aznar-Siguan y Bresch, 2019) a partir de mapas por periodo de retorno.

    Cada mapa de profundidad (`profundidades`, {periodo: profundidad en cada punto}) es un evento con frecuencia
    1/T menos la del periodo siguiente, como se hace con los mapas del JRC; el daño sigue la curva
    profundidad–daño `curva` ({"profundidad_m": [...], "fraccion": [...]}). Con `elevaciones_m` evalúa la medida de
    elevar las edificaciones marcadas en `region` (1 = se eleva) esos metros. Requiere el paquete `climada`.
    """
    from scipy import sparse
    from climada.engine import ImpactCalc
    from climada.entity import Exposures, ImpactFunc, ImpactFuncSet
    from climada.entity.measures import Measure
    from climada.hazard import Centroids, Hazard

    rps = sorted(profundidades)
    prof = np.vstack([np.nan_to_num(np.asarray(profundidades[r], dtype=float)) for r in rps])
    frecuencia = np.array([1 / r - (1 / rps[i + 1] if i + 1 < len(rps) else 0) for i, r in enumerate(rps)])
    amenaza = Hazard(haz_type="RF", units="m", centroids=Centroids(lat=np.asarray(lat), lon=np.asarray(lon)),
                     event_id=np.arange(1, len(rps) + 1), event_name=[f"T{r}" for r in rps], frequency=frecuencia,
                     intensity=sparse.csr_matrix(prof), fraction=sparse.csr_matrix((prof > 0).astype(float)))
    amenaza.check()
    funcion = ImpactFunc(haz_type="RF", id=1, intensity=np.asarray(curva["profundidad_m"], dtype=float),
                         mdd=np.asarray(curva["fraccion"], dtype=float), paa=np.ones(len(curva["fraccion"])), intensity_unit="m")
    funciones = ImpactFuncSet([funcion])
    expo = Exposures(pd.DataFrame({"latitude": np.asarray(lat), "longitude": np.asarray(lon), "value": np.asarray(valores, dtype=float),
                                   "impf_RF": 1, "region_id": np.ones(len(lon), dtype=int) if region is None else np.asarray(region, dtype=int)}))
    expo.assign_centroids(amenaza, threshold=1)
    imp = ImpactCalc(expo, funciones, amenaza).impact(save_mat=False)
    curva_exc = imp.calc_freq_curve(rps)
    out = {"pae": float(imp.aai_agg), "por_periodo": pd.Series(curva_exc.impact, index=curva_exc.return_per),
           "pae_por_punto": np.asarray(imp.eai_exp)}
    filas = []
    for h in elevaciones_m or []:
        medida = Measure(name=f"elevar {h:g} m", haz_type="RF", hazard_inten_imp=(1, -h), exp_region_id=[1])
        imp_m, _ = medida.calc_impact(expo, funciones, amenaza)
        filas.append({"medida": medida.name, "pae": float(imp_m.aai_agg), "reduccion_%": 100 * (1 - imp_m.aai_agg / imp.aai_agg)})
    out["medidas"] = pd.DataFrame(filas).set_index("medida") if filas else pd.DataFrame()
    return out
