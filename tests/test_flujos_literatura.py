"""Pruebas de los métodos tomados de la literatura (página 1.8) con datos sintéticos."""
import numpy as np
import pandas as pd

from leticia import clima, hidro, pronostico, salud
from leticia.fuentes import _sin_tildes


def _nivel_sintetico(inicio="2000-01-01", fin="2009-12-31"):
    idx = pd.date_range(inicio, fin)
    return pd.Series(1100 + 500 * np.cos(2 * np.pi * (idx.dayofyear - 135) / 365.25), index=idx)


def test_dias_bajo_p80_promedia_un_quinto_del_anio():
    s = _nivel_sintetico()
    dur, umbral = hidro.dias_bajo_referencia(s)
    completos = dur[dur["completo"]]
    assert abs(umbral - np.percentile(s, 20)) < 5
    assert 65 <= completos["dias_bajo"].median() <= 80


def test_dias_bajo_p80_marca_temporadas_incompletas():
    s = _nivel_sintetico()
    s["2005-08-01":"2005-10-31"] = np.nan
    dur, _ = hidro.dias_bajo_referencia(s)
    assert not dur.loc[2005, "completo"]
    assert dur.loc[2004, "completo"]


def test_p80_ponderado_no_se_sesga_con_vacios_en_aguas_bajas():
    s = _nivel_sintetico()
    _, completo = hidro.dias_bajo_referencia(s)
    s2 = s.copy()
    s2[s2.index.month.isin([9, 10]) & (s2.index.year % 2 == 0)] = np.nan   # faltan aguas bajas en la mitad de los años
    _, con_vacios = hidro.dias_bajo_referencia(s2)
    assert abs(con_vacios - completo) < 20


def test_comparar_simulacion_encuentra_el_desfase():
    obs = _nivel_sintetico("1990-01-01", "2009-12-31")
    sim = (obs.shift(-10) * 40).dropna()          # «caudal» que se adelanta 10 días al nivel
    res, picos = hidro.comparar_simulacion(obs, sim)
    assert res["desfase_optimo_dias"] == 10
    assert res["spearman_desfase"] > 0.99
    assert (picos["error_dias"] <= 0).all()


def test_regresion_validada_recupera_relacion_lineal():
    x = pd.Series(np.linspace(-1, 1, 25), index=range(2000, 2025))
    y = 2 + 3 * x
    pred, coef = pronostico.regresion_validada(y, x.to_frame("x"))
    ref, _ = pronostico.regresion_validada(y, x.to_frame("x").iloc[:, :0])
    assert np.allclose(coef, [2, 3])
    assert pronostico.habilidad(y, pred, ref)["habilidad"] > 0.99


def test_media_meses_solo_anios_completos():
    idx = pd.date_range("2000-01-01", "2001-04-01", freq="MS")
    s = pd.Series(np.arange(len(idx), dtype=float), index=idx)
    m = pronostico.media_meses(s, [3, 4, 5])
    assert list(m.index) == [2000]
    assert m.loc[2000] == 3.0


def test_casos_mensuales_conserva_el_total():
    semanas = pd.date_range("2015-01-04", periods=104, freq="7D")
    s = pd.Series(np.random.default_rng(4).poisson(5, len(semanas)).astype(float), index=semanas)
    m = salud.casos_mensuales(s)
    assert m.sum() == s.sum()
    assert m.index.freqstr.startswith("MS")


def test_modelo_autorregresivo_gana_con_persistencia():
    rng = np.random.default_rng(5)
    idx = pd.date_range("2005-01-01", "2020-12-01", freq="MS")
    z = np.zeros(len(idx))
    for i in range(1, len(idx)):
        z[i] = 0.9 * z[i - 1] + rng.normal(0, 0.5)
    casos = pd.Series(np.round(np.expm1(3 + z)).clip(0), index=idx)
    X = pd.DataFrame({"ruido": rng.normal(size=len(idx))}, index=idx)
    hab, pred = salud.modelos_dengue(casos, X, 1)
    assert hab.loc["autorregresivo", "habilidad"] > 0.3
    assert hab.loc["autorregresivo", "habilidad"] > hab.loc["hidroclimático", "habilidad"]
    assert "observado" in pred


def test_aptitud_termica_clasifica_segun_mordecai():
    t = pd.Series([15.0, 24.0, 27.0, 30.0, 36.0])
    c = salud.aptitud_termica(t, 17.8, (26, 29), 34.6)
    assert list(c.astype(str)) == ["sin transmisión (frío)", "subóptima (fresca)", "máxima transmisión",
                                   "sobre el óptimo", "sin transmisión (calor)"]


def test_utci_a_la_sombra_valores_de_referencia():
    u = clima.utci([30.0, 35.0], [1.0, 1.0], [24.0, 25.0])
    assert abs(u[0] - 32.3) < 0.3
    assert abs(u[1] - 37.3) < 0.3


def test_estres_termico_diario_cuenta_horas():
    idx = pd.date_range("2020-01-01", periods=48, freq="h")
    hora = np.asarray(idx.hour)
    h = pd.DataFrame({"temperature_2m": 24 + 8 * np.sin(np.pi * (hora - 6) / 12).clip(0), "dew_point_2m": 22.0,
                      "wind_speed_10m": 1.5}, index=idx)
    d = clima.estres_termico_diario(h, {"moderado": 26, "fuerte": 32})
    assert len(d) == 2
    assert (d["horas_moderado"] >= d["horas_fuerte"]).all()
    assert (d["horas_fuerte"] > 0).all()


def test_sin_tildes():
    assert _sin_tildes("Leticia") == "LETICIA"
    assert _sin_tildes("Puerto Nariño") == "PUERTO NARINO"
