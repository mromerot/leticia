"""Hidrología del río Amazonas en Leticia: control de calidad, extremos y tendencias."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from .config import parametros


def limpiar_nivel(s: pd.Series) -> pd.Series:
    """Quita registros imposibles: ceros, valores bajo el mínimo válido y saltos frente a la mediana móvil."""
    p = parametros()["hidrologia"]
    s = s.astype(float).copy()
    s = s[~s.index.duplicated()].asfreq("D")  # días sin dato como NaN: las gráficas no unen lagunas
    s[s < p["nivel_min_valido_cm"]] = np.nan
    for ini, fin in p.get("periodos_excluidos", []):
        s[ini:fin] = np.nan
    med = s.rolling(15, center=True, min_periods=5).median()
    s[(s - med).abs() > p["salto_max_cm_dia"]] = np.nan
    return s


def extremos_anuales(s: pd.Series, tipo: str = "max") -> pd.DataFrame:
    """Máximo (aguas altas) o mínimo (aguas bajas) de cada año, solo si la temporada tiene datos suficientes."""
    p = parametros()["hidrologia"]
    meses = p["temporada_altas"] if tipo == "max" else p["temporada_bajas"]
    temporada = s[s.index.month.isin(meses)].dropna()
    g = temporada.groupby(temporada.index.year)
    df = pd.DataFrame({"valor": g.max() if tipo == "max" else g.min(), "dias": g.count(),
                       "fecha": g.idxmax() if tipo == "max" else g.idxmin()})
    return df[df["dias"] >= p["dias_min_temporada"]]


def _gev_lmomentos(x: np.ndarray) -> tuple:
    """Parámetros GEV por L-momentos (Hosking, 1985), en la convención de SciPy (c, loc, scale).

    Los L-momentos son más estables que la máxima verosimilitud con muestras cortas o con un valor
    atípico como la vaciante de 2024, que lleva la verosimilitud a soluciones degeneradas.
    """
    from math import gamma, log

    x = np.sort(np.asarray(x, dtype=float))
    n = len(x)
    i = np.arange(1, n + 1)
    b0 = x.mean()
    b1 = np.sum((i - 1) / (n - 1) * x) / n
    b2 = np.sum((i - 1) * (i - 2) / ((n - 1) * (n - 2)) * x) / n
    l1, l2, l3 = b0, 2 * b1 - b0, 6 * b2 - 6 * b1 + b0
    t3 = l3 / l2
    z = 2 / (3 + t3) - log(2) / log(3)
    k = 7.8590 * z + 2.9554 * z ** 2
    alfa = l2 * k / ((1 - 2 ** (-k)) * gamma(1 + k))
    xi = l1 - alfa * (1 - gamma(1 + k)) / k
    return (k, xi, alfa)


def ajustar_gev(x: np.ndarray, minimos: bool = False, metodo: str = "lmom") -> tuple:
    """Ajusta una GEV por L-momentos (por defecto) o máxima verosimilitud. Para mínimos se ajusta sobre −x."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    y = -x if minimos else x
    return _gev_lmomentos(y) if metodo == "lmom" else stats.genextreme.fit(y)


def nivel_retorno(params: tuple, periodos, minimos: bool = False) -> np.ndarray:
    """Nivel con periodo de retorno T (años). En mínimos: nivel tan bajo que se alcanza 1 vez cada T años."""
    T = np.asarray(periodos, dtype=float)
    q = stats.genextreme.ppf(1 - 1 / T, *params)
    return -q if minimos else q


def niveles_retorno_ic(x, periodos, minimos: bool = False, n: int = 500, semilla: int = 1) -> pd.DataFrame:
    """Niveles de retorno con intervalo de confianza del 90 % por remuestreo (bootstrap)."""
    rng = np.random.default_rng(semilla)
    x = np.asarray(x, dtype=float)
    base = nivel_retorno(ajustar_gev(x, minimos), periodos, minimos)
    muestras = []
    for _ in range(n):
        try:
            muestras.append(nivel_retorno(ajustar_gev(rng.choice(x, len(x)), minimos), periodos, minimos))
        except Exception:  # noqa: BLE001
            continue
    m = np.array(muestras)
    return pd.DataFrame({"periodo_retorno": periodos, "nivel": base, "ic5": np.nanpercentile(m, 5, axis=0),
                         "ic95": np.nanpercentile(m, 95, axis=0)}).set_index("periodo_retorno")


def periodo_retorno_empirico(x, minimos: bool = False) -> pd.Series:
    """Periodo de retorno empírico (posición de Weibull) de cada valor observado."""
    x = pd.Series(x).dropna()
    rango = x.rank(ascending=minimos)
    return (len(x) + 1) / rango


def mann_kendall(x) -> dict:
    """Prueba de tendencia de Mann-Kendall y pendiente de Sen (unidades de x por paso)."""
    x = pd.Series(x).dropna()
    t = np.asarray(x.index, dtype=float)
    v = x.to_numpy(dtype=float)
    n = len(v)
    s = sum(np.sign(v[j] - v[i]) for i in range(n - 1) for j in range(i + 1, n))
    var = n * (n - 1) * (2 * n + 5) / 18
    z = (s - np.sign(s)) / np.sqrt(var) if s != 0 else 0.0
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    pendientes = [(v[j] - v[i]) / (t[j] - t[i]) for i in range(n - 1) for j in range(i + 1, n) if t[j] != t[i]]
    return {"n": n, "S": s, "z": z, "p": p, "sen": float(np.median(pendientes)) if pendientes else np.nan}


def dias_bajo_umbral(s: pd.Series, umbral: float, debajo: bool = True, cobertura_min: float = 0.8) -> pd.Series:
    """Días por año con el nivel por debajo (o encima) de un umbral.

    Solo se usan los años en que la temporada de aguas bajas (o altas) tiene al menos `cobertura_min`
    de los días con dato, para no contar como «cero días» un año con la vaciante sin registrar.
    """
    p = parametros()["hidrologia"]
    meses = p["temporada_bajas"] if debajo else p["temporada_altas"]
    s = s.dropna()
    cond = (s < umbral) if debajo else (s > umbral)
    temporada = s[s.index.month.isin(meses)]
    dias_temporada = pd.Series(pd.date_range("2001-01-01", "2001-12-31")).dt.month.isin(meses).sum()
    cobertura = temporada.groupby(temporada.index.year).size() / dias_temporada
    conteo = cond.groupby(s.index.year).sum()
    return conteo[cobertura.reindex(conteo.index).fillna(0) >= cobertura_min]


def climatologia_diaria(s: pd.Series, base: tuple[int, int] | None = None) -> pd.DataFrame:
    """Percentiles por día del año (p10, p50, p90, mín, máx) para comparar un año con su historia."""
    if base:
        s = s[(s.index.year >= base[0]) & (s.index.year <= base[1])]
    doy = np.minimum(np.asarray(s.index.dayofyear), 365)
    g = s.groupby(doy)
    return pd.DataFrame({"min": g.min(), "p10": g.quantile(0.10), "p50": g.median(), "p90": g.quantile(0.90), "max": g.max()})


def relacion_nivel_caudal(nivel: pd.Series, caudal: pd.Series, grado: int = 2):
    """Ajuste polinómico nivel ~ caudal (días comunes) para pasar del caudal de GloFAS a la regla de Leticia."""
    df = pd.concat({"nivel": nivel, "caudal": caudal}, axis=1).dropna()
    coef = np.polyfit(df["caudal"], df["nivel"], grado)
    pred = np.polyval(coef, df["caudal"])
    r2 = 1 - ((df["nivel"] - pred) ** 2).sum() / ((df["nivel"] - df["nivel"].mean()) ** 2).sum()
    return coef, float(r2), df


def dias_bajo_referencia(s: pd.Series, excedencia: float = 80, mes_inicio: int = 12, cobertura_min: float = 0.8,
                         base: tuple[int, int] | None = None) -> tuple[pd.DataFrame, float]:
    """Días por año hidrológico con el nivel por debajo del P80 de la curva de duración (Santos de Lima et al., 2024).

    El P80 es el nivel igualado o superado el 80 % del tiempo, es decir, el percentil 20 de los niveles diarios. Como
    a la serie le faltan sobre todo días de aguas bajas, cada dato pesa 1/(datos de su día del año): así la curva de
    duración representa por igual todas las épocas del año. El año hidrológico empieza en `mes_inicio` (diciembre) y
    se nombra por el año en que termina. Devuelve, por año, los días bajo el umbral, la cobertura de la temporada de
    aguas bajas y si el año está completo (cobertura ≥ `cobertura_min`); en los incompletos el conteo es un mínimo.
    """
    meses = parametros()["hidrologia"]["temporada_bajas"]
    s = s.dropna()
    ref = s if base is None else s[(s.index.year >= base[0]) & (s.index.year <= base[1])]
    doy = np.minimum(np.asarray(ref.index.dayofyear), 365)
    peso = 1 / pd.Series(doy).map(pd.Series(doy).value_counts()).to_numpy()
    orden = np.argsort(ref.to_numpy())
    acumulado = np.cumsum(peso[orden]) / peso.sum()
    umbral = float(ref.to_numpy()[orden][np.searchsorted(acumulado, 1 - excedencia / 100)])
    anio = s.index.year + ((s.index.month >= mes_inicio) & (mes_inicio > 1)).astype(int)
    dias_temporada = pd.Series(pd.date_range("2001-01-01", "2001-12-31")).dt.month.isin(meses).sum()
    out = pd.DataFrame({"dias_bajo": (s < umbral).groupby(anio).sum(),
                        "cobertura": pd.Series(s.index.month.isin(meses), index=s.index).groupby(anio).sum() / dias_temporada})
    out["completo"] = out["cobertura"] >= cobertura_min
    return out.rename_axis("anio_hidrologico"), umbral


def comparar_simulacion(obs: pd.Series, sim: pd.Series, percentil_evento: float = 95, desfase_max: int = 30) -> tuple[dict, pd.DataFrame]:
    """Compara una serie diaria simulada (p. ej., caudal de GloFAS) con una observada de otra magnitud (nivel).

    Como la relación nivel–caudal es monótona, usa medidas de rango y de calendario en lugar del KGE, que exige
    caudal observado: correlación de Spearman diaria y de los máximos anuales, desfase que maximiza la correlación,
    error en la fecha del pico anual, correlación de los máximos y de los mínimos anuales y detección de los días
    sobre el percentil `percentil_evento` de cada serie (después de corregir el desfase).
    Devuelve un resumen y una tabla por año con las fechas de los picos.
    """
    df = pd.concat({"obs": obs, "sim": sim}, axis=1).dropna()
    rho = float(stats.spearmanr(df["obs"], df["sim"])[0])
    desfases = {d: stats.spearmanr(*pd.concat([obs, sim.shift(d)], axis=1).dropna().T.values)[0] for d in range(-desfase_max, desfase_max + 1)}
    mejor = max(desfases, key=desfases.get)
    meses = parametros()["hidrologia"]["temporada_altas"]
    alta = df[df.index.month.isin(meses)]
    g = alta.groupby(alta.index.year)
    anual = pd.DataFrame({"pico_obs": g["obs"].idxmax(), "pico_sim": g["sim"].idxmax(), "max_obs": g["obs"].max(),
                          "max_sim": g["sim"].max(), "dias": g.size()})
    anual = anual[anual["dias"] >= parametros()["hidrologia"]["dias_min_temporada"]]
    anual["error_dias"] = (anual["pico_sim"] - anual["pico_obs"]).dt.days
    baja = df[df.index.month.isin(parametros()["hidrologia"]["temporada_bajas"])]
    gb = baja.groupby(baja.index.year)
    minimos = pd.DataFrame({"obs": gb["obs"].min(), "sim": gb["sim"].min()})[gb.size() >= parametros()["hidrologia"]["dias_min_temporada"]]
    dfd = pd.concat({"obs": obs, "sim": sim.shift(mejor)}, axis=1).dropna()   # eventos con el desfase corregido
    ev_obs = dfd["obs"] > np.percentile(dfd["obs"], percentil_evento)
    ev_sim = dfd["sim"] > np.percentile(dfd["sim"], percentil_evento)
    aciertos, fallas, falsas = int((ev_obs & ev_sim).sum()), int((ev_obs & ~ev_sim).sum()), int((~ev_obs & ev_sim).sum())
    resumen = {"dias_comunes": len(df), "spearman_diario": rho, "desfase_optimo_dias": int(mejor), "spearman_desfase": float(desfases[mejor]),
               "spearman_maximos_anuales": float(stats.spearmanr(anual["max_obs"], anual["max_sim"])[0]), "anios": len(anual),
               "spearman_minimos_anuales": float(stats.spearmanr(minimos["obs"], minimos["sim"])[0]), "anios_minimos": len(minimos),
               "error_pico_mediano_dias": float(anual["error_dias"].median()), "error_pico_absoluto_dias": float(anual["error_dias"].abs().median()),
               "probabilidad_deteccion": aciertos / max(aciertos + fallas, 1), "razon_falsas_alarmas": falsas / max(aciertos + falsas, 1)}
    return resumen, anual
