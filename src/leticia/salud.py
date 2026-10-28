"""Dengue y clima: series mensuales, rezagos y pronóstico estadístico a 1–6 meses (Beal et al., 2025)."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from .clima import suma_mensual
from .pronostico import habilidad, regresion_validada


def casos_mensuales(semanal: pd.Series) -> pd.Series:
    """Suma mensual de casos semanales; cada semana cuenta en el mes de su día central (miércoles)."""
    s = semanal.copy()
    s.index = s.index + pd.Timedelta(days=3)
    return s.resample("MS").sum()


def anomalia_mensual(s: pd.Series, base: tuple[int, int] | None = None) -> pd.Series:
    """Anomalía estandarizada por mes calendario (resta la media y divide por la desviación de cada mes)."""
    ref = s if base is None else s[(s.index.year >= base[0]) & (s.index.year <= base[1])]
    media = ref.groupby(ref.index.month).mean()
    desv = ref.groupby(ref.index.month).std()
    return (s - media.reindex(s.index.month).to_numpy()) / desv.reindex(s.index.month).to_numpy()


def predictores_mensuales(diario: pd.DataFrame, indices: dict[str, pd.Series], base: tuple[int, int] | None = None) -> pd.DataFrame:
    """Anomalías mensuales estandarizadas de temperatura, lluvia y humedad (ERA5 diario) e índices oceánicos."""
    n = diario["temperature_2m_mean"].resample("MS").count()
    completos = n[n == n.index.days_in_month].index
    local = pd.DataFrame({
        "temperatura": diario["temperature_2m_mean"].resample("MS").mean(),
        "lluvia": suma_mensual(diario["precipitation_sum"]),
        "humedad": diario["relative_humidity_2m_mean"].resample("MS").mean(),
    }).loc[completos]
    out = {c: anomalia_mensual(local[c], base) for c in local}
    out.update({k: v.asfreq("MS") for k, v in indices.items()})   # el ONI y el TNA ya son anomalías
    return pd.DataFrame(out)


def tabla_rezagos(y: pd.Series, X: pd.DataFrame, rezagos=range(0, 7)) -> pd.DataFrame:
    """Correlación de Spearman entre `y` y cada predictor adelantado `k` meses (el predictor precede a `y`)."""
    filas = {}
    for k in rezagos:
        filas[k] = {c: stats.spearmanr(*pd.concat([y, X[c].shift(k)], axis=1).dropna().T.values)[0] for c in X}
    return pd.DataFrame(filas).T.rename_axis("rezago (meses)")


def modelos_dengue(casos: pd.Series, X: pd.DataFrame, rezago: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compara modelos de pronóstico de log(1 + casos mensuales) con `rezago` meses de anticipación.

    Todos incluyen el ciclo estacional (un término por mes) y se validan dejando fuera un año completo cada vez:
    - climatología: solo el ciclo estacional (referencia);
    - autorregresivo: ciclo + casos de hace `rezago` meses;
    - oceánico: ciclo + ONI y TNA de hace `rezago` meses (la TSM fue el mejor predictor a 3–6 meses en Beal et al.);
    - hidroclimático: ciclo + todos los predictores de hace `rezago` meses (temperatura, lluvia, humedad, ONI y TNA);
    - combinado: ambos.
    Devuelve la habilidad de cada modelo y sus predicciones (en casos).
    """
    y = np.log1p(casos.astype(float)).rename("y")
    mes = pd.get_dummies(y.index.month, prefix="m", drop_first=True, dtype=float).set_index(y.index)
    ar = y.shift(rezago).rename("casos_previos").to_frame()
    hc = X.shift(rezago).reindex(y.index)
    oceano = hc[[c for c in ("ONI", "TNA") if c in hc]]
    conjuntos = {"climatología": mes, "autorregresivo": mes.join(ar), "oceánico": mes.join(oceano), "hidroclimático": mes.join(hc),
                 "combinado": mes.join(ar).join(hc)}
    comunes = pd.concat([y, ar, hc], axis=1).dropna().index      # mismos meses para todos los modelos
    anio = pd.Series(comunes.year, index=comunes)
    pred = {n: regresion_validada(y.loc[comunes], c.loc[comunes], anio)[0] for n, c in conjuntos.items()}
    filas = {n: habilidad(y.loc[comunes], p, pred["climatología"]) for n, p in pred.items()}
    return pd.DataFrame(filas).T, np.expm1(pd.DataFrame(pred)).assign(observado=casos.loc[comunes])


def aptitud_termica(temperatura: pd.Series, inferior: float, rango_maximo: tuple[float, float], superior: float) -> pd.Series:
    """Clasifica temperaturas medias según la respuesta térmica de la transmisión por Aedes (Mordecai et al., 2017).

    Entre `inferior` y `superior` hay transmisión; es máxima en `rango_maximo` y decae por encima de ese rango.
    """
    return pd.cut(temperatura, [-np.inf, inferior, rango_maximo[0], rango_maximo[1], superior, np.inf],
                  labels=["sin transmisión (frío)", "subóptima (fresca)", "máxima transmisión", "sobre el óptimo", "sin transmisión (calor)"])
