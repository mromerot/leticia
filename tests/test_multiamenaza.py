import numpy as np
import pandas as pd

from leticia import multiamenaza as mm


def test_maximo_no_suma():
    a, b = np.array([0.5, 0.0, 1.0]), np.array([0.3, 0.2, 1.0])
    assert list(mm.combinar_maximo(a, b)) == [0.5, 0.2, 1.0]
    assert list(mm.combinar_suma_acotada(a, b)) == [0.8, 0.2, 1.0]


def test_razon_suma_maximo_mayor_que_uno_si_se_solapan():
    assert mm.razon_suma_maximo([0.5, 0.0], [0.3, 0.2], [100, 100]) > 1
    assert mm.razon_suma_maximo([0.5, 0.0], [0.0, 0.2], [100, 100]) == 1.0 or mm.razon_suma_maximo([0.5, 0.0], [0.0, 0.2], [100, 100]) > 0.99


def test_bandas_ordenadas_en_danio():
    prof = np.array([0.5, 1.0, 2.0])
    lo, me, hi = (mm.fraccion_danio_banda(prof, b) for b in mm.BANDAS)
    assert (lo <= me).all() and (me <= hi).all() and (hi <= 1).all()


def test_encharcamiento_crece_con_el_periodo_y_la_banda():
    d = np.array([2.0])
    assert mm.profundidad_encharcamiento(d, 100)[0] > mm.profundidad_encharcamiento(d, 2)[0]
    assert mm.profundidad_encharcamiento(d, 10, "maximo")[0] > mm.profundidad_encharcamiento(d, 10, "minimo")[0]


def test_fase_enso():
    idx = pd.date_range("2015-01-01", "2016-12-01", freq="MS")
    oni = pd.Series(np.where(idx.year == 2015, 1.5, -1.0), index=idx)   # el valor de enero (DJF) define la fase
    f = mm.fase_enso(oni)
    assert f[2015] == "El Niño" and f[2016] == "La Niña"


def test_vendaval_anual_incluye_anios_sin_evento():
    ev = pd.DataFrame({"averiadas": [10, 0], "destruidas": [0, 2]}, index=pd.to_datetime(["2021-05-01", "2023-03-01"]))
    s = mm.anual_empirico_vendaval(ev, 100.0, 0.1, range(2020, 2024))
    assert s[2020] == 0 and s[2021] == 100.0 and s[2023] == 200.0


def test_curva_empirica_probabilidades():
    c = mm.curva_excedencia_empirica(pd.Series([1.0, 5.0, 3.0]))
    assert list(c["valor"]) == [5.0, 3.0, 1.0] and c["prob_excedencia"].iloc[0] == 0.25
