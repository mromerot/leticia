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
