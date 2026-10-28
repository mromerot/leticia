import numpy as np
import pandas as pd

from leticia import clima


def test_olas_calor_cuenta_rachas():
    idx = pd.date_range("2020-01-01", "2020-12-31")
    t = pd.Series(30.0, index=idx)
    t["2020-03-01":"2020-03-05"] = 35
    t["2020-06-01":"2020-06-02"] = 35
    o = clima.olas_calor(t, 33, 3)
    assert o.loc[2020, "dias_sobre_umbral"] == 7
    assert o.loc[2020, "olas"] == 1
    assert o.loc[2020, "ola_mas_larga"] == 5


def test_spi_estandarizado():
    rng = np.random.default_rng(0)
    idx = pd.date_range("1981-01-01", "2020-12-31")
    p = pd.Series(rng.gamma(0.8, 10, len(idx)), index=idx)
    s = clima.spi(p, 3).dropna()
    assert abs(s.mean()) < 0.15
    assert 0.8 < s.std() < 1.2


def test_mes_incompleto_se_descarta():
    idx = pd.date_range("2000-01-01", "2000-03-15")
    m = clima._mensual_completo(pd.Series(1.0, index=idx))
    assert list(m.index.month) == [1, 2]


def test_indice_calor_mayor_que_temperatura_en_humedo():
    hi = clima.indice_calor(pd.Series([32.0]), pd.Series([80.0]))
    assert hi.iloc[0] > 38
