import numpy as np
import pandas as pd
from scipy import stats

from leticia import hidro


def test_gev_lmomentos_recupera_parametros():
    rng = np.random.default_rng(0)
    x = stats.genextreme.rvs(0.1, loc=100, scale=10, size=4000, random_state=rng)
    c, loc, esc = hidro.ajustar_gev(x)
    assert abs(c - 0.1) < 0.05
    assert abs(loc - 100) < 1.5
    assert abs(esc - 10) < 1.0


def test_niveles_retorno_crecen_con_el_periodo():
    rng = np.random.default_rng(1)
    x = stats.genextreme.rvs(-0.05, loc=1700, scale=60, size=40, random_state=rng)
    r = hidro.niveles_retorno_ic(x, [2, 10, 100], n=50)
    assert r["nivel"].is_monotonic_increasing


def test_minimos_retorno_decrecen():
    rng = np.random.default_rng(2)
    x = 800 - stats.genextreme.rvs(0.0, loc=0, scale=80, size=40, random_state=rng)
    r = hidro.niveles_retorno_ic(x, [2, 10, 100], minimos=True, n=50)
    assert r["nivel"].is_monotonic_decreasing


def test_mann_kendall_detecta_tendencia():
    s = pd.Series(np.arange(30) * 2.0 + np.random.default_rng(3).normal(0, 1, 30), index=range(1990, 2020))
    mk = hidro.mann_kendall(s)
    assert mk["p"] < 0.01
    assert 1.5 < mk["sen"] < 2.5


def test_limpiar_nivel_quita_ceros_saltos_y_periodos_excluidos():
    idx = pd.date_range("2006-01-01", "2008-12-31")
    s = pd.Series(1000.0 + 500 * np.sin(np.arange(len(idx)) / 58), index=idx)
    s.iloc[10] = 0
    s.iloc[400] = s.iloc[400] + 900
    limpio = hidro.limpiar_nivel(s)
    assert np.isnan(limpio.iloc[10]) and np.isnan(limpio.iloc[400])
    assert limpio["2007"].isna().all()
    assert limpio["2008"].notna().all()


def test_dias_bajo_umbral_exige_cobertura():
    idx = pd.date_range("2020-01-01", "2021-12-31")
    s = pd.Series(700.0, index=idx)
    s["2020-09-01":"2020-09-10"] = 300
    s = s.drop(s["2021-08-01":"2021-11-30"].index)
    d = hidro.dias_bajo_umbral(s, 400)
    assert d.loc[2020] == 10
    assert 2021 not in d.index
