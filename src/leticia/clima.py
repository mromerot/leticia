"""Índices climáticos a partir de series diarias (ERA5): calor, sequía, lluvia y viento."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def umbral_percentil(s: pd.Series, q: float, base: tuple[int, int] | None = None) -> float:
    if base:
        s = s[(s.index.year >= base[0]) & (s.index.year <= base[1])]
    return float(np.nanpercentile(s, q))


def rachas(cond: pd.Series, minimo: int) -> pd.DataFrame:
    """Rachas de días consecutivos en que `cond` es verdadera y que duran al menos `minimo` días."""
    cond = cond.fillna(False).astype(bool)
    grupo = (cond != cond.shift()).cumsum()
    r = cond.groupby(grupo).agg(["first", "size"])
    r = r[r["first"] & (r["size"] >= minimo)]
    inicios = cond.groupby(grupo).apply(lambda x: x.index[0])
    return pd.DataFrame({"inicio": inicios.loc[r.index].values, "dias": r["size"].values})


def olas_calor(tmax: pd.Series, umbral: float, minimo: int = 3) -> pd.DataFrame:
    """Días sobre el umbral, número de olas, ola más larga y días en ola por año."""
    sobre = tmax > umbral
    r = rachas(sobre, minimo)
    r["anio"] = pd.to_datetime(r["inicio"]).dt.year
    anios = sorted(set(tmax.index.year))
    out = pd.DataFrame(index=pd.Index(anios, name="anio"))
    out["dias_sobre_umbral"] = sobre.groupby(tmax.index.year).sum()
    out["olas"] = r.groupby("anio").size()
    out["ola_mas_larga"] = r.groupby("anio")["dias"].max()
    out["dias_en_ola"] = r.groupby("anio")["dias"].sum()
    return out.fillna(0)


def indice_calor(t_c: pd.Series, hr: pd.Series) -> pd.Series:
    """Índice de calor (Rothfusz/NWS) en °C a partir de temperatura (°C) y humedad relativa (%)."""
    t = t_c * 9 / 5 + 32
    hi = (-42.379 + 2.04901523 * t + 10.14333127 * hr - 0.22475541 * t * hr - 6.83783e-3 * t ** 2
          - 5.481717e-2 * hr ** 2 + 1.22874e-3 * t ** 2 * hr + 8.5282e-4 * t * hr ** 2 - 1.99e-6 * t ** 2 * hr ** 2)
    simple = 0.5 * (t + 61 + (t - 68) * 1.2 + hr * 0.094)
    hi = hi.where((simple + t) / 2 >= 80, simple)
    return (hi - 32) * 5 / 9


def humedad_relativa(t_c: pd.Series, td_c: pd.Series) -> pd.Series:
    """Humedad relativa (%) a partir de temperatura y punto de rocío (Magnus)."""
    a, b = 17.625, 243.04
    return (100 * np.exp(a * td_c / (b + td_c)) / np.exp(a * t_c / (b + t_c))).clip(0, 100)


def _mensual_completo(diaria: pd.Series) -> pd.Series:
    """Suma mensual solo de meses completos (el último mes en curso se descarta para no subestimar la lluvia)."""
    suma = diaria.resample("MS").sum(min_count=1)
    n = diaria.resample("MS").count()
    return suma[n == suma.index.days_in_month]


def spi(precip_diaria: pd.Series, escala_meses: int = 3, base: tuple[int, int] | None = None) -> pd.Series:
    """Índice de Precipitación Estandarizado (SPI) mensual con ajuste gamma por mes calendario."""
    m = _mensual_completo(precip_diaria)
    acum = m.rolling(escala_meses, min_periods=escala_meses).sum()
    out = pd.Series(np.nan, index=acum.index)
    for mes in range(1, 13):
        sel = acum[acum.index.month == mes].dropna()
        ref = sel if not base else sel[(sel.index.year >= base[0]) & (sel.index.year <= base[1])]
        ceros = (ref == 0).mean()
        a, loc, esc = stats.gamma.fit(ref[ref > 0], floc=0)
        prob = ceros + (1 - ceros) * stats.gamma.cdf(sel, a, loc=loc, scale=esc)
        out.loc[sel.index] = stats.norm.ppf(np.clip(prob, 1e-6, 1 - 1e-6))
    return out


def balance_hidrico_spei(precip: pd.Series, et0: pd.Series, escala_meses: int = 3,
                         base: tuple[int, int] | None = None) -> pd.Series:
    """Índice tipo SPEI: balance P − ET0 acumulado y estandarizado con una log-logística por mes."""
    d = _mensual_completo(precip - et0)
    acum = d.rolling(escala_meses, min_periods=escala_meses).sum()
    out = pd.Series(np.nan, index=acum.index)
    for mes in range(1, 13):
        sel = acum[acum.index.month == mes].dropna()
        ref = sel if not base else sel[(sel.index.year >= base[0]) & (sel.index.year <= base[1])]
        params = stats.fisk.fit(ref)
        out.loc[sel.index] = stats.norm.ppf(np.clip(stats.fisk.cdf(sel, *params), 1e-6, 1 - 1e-6))
    return out


def max_dias_secos(precip: pd.Series, umbral_mm: float = 1.0) -> pd.Series:
    """Máximo de días secos consecutivos por año (CDD)."""
    seco = precip < umbral_mm
    grupo = (seco != seco.shift()).cumsum()
    largo = seco.groupby(grupo).transform("size").where(seco, 0)
    return largo.groupby(precip.index.year).max()


def indices_lluvia(precip: pd.Series, umbral_fuerte: float = 50) -> pd.DataFrame:
    """Rx1day, Rx5day, días ≥ 20 mm, días ≥ umbral fuerte y total anual."""
    g = precip.groupby(precip.index.year)
    return pd.DataFrame({
        "total_mm": g.sum(), "rx1day": g.max(), "rx5day": precip.rolling(5).sum().groupby(precip.index.year).max(),
        "r20mm": (precip >= 20).groupby(precip.index.year).sum(),
        f"r{int(umbral_fuerte)}mm": (precip >= umbral_fuerte).groupby(precip.index.year).sum(),
    })


def anomalia_anual(s: pd.Series, base: tuple[int, int], como: str = "mean") -> pd.Series:
    a = s.groupby(s.index.year).agg(como)
    return a - a.loc[base[0]:base[1]].mean()
