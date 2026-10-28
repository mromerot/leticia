import numpy as np
import pandas as pd

from leticia import riesgo
from leticia.fuentes import _quadkey, _teselas_10grados


def test_curva_de_danio():
    f = riesgo.fraccion_danio([0, 0.5, 10])
    assert f[0] == 0 and 0.4 < f[1] < 0.6 and f[2] == 1


def test_perdida_anual_esperada_constante():
    # pérdida de 100 para cualquier evento entre T=2 y T=100 → PAE ≈ 100 × (1/1 − 1/100) con el cierre en p=1
    pae = riesgo.perdida_anual_esperada(pd.Series([100.0, 100.0], index=[2, 100]))
    assert 50 < pae < 100


def test_matriz_riesgo():
    a = pd.Series(pd.Categorical(["Muy alta", "Muy baja", "Media"], categories=riesgo.CLASES))
    v = pd.Series(pd.Categorical(["Muy alta", "Muy alta", "Media"], categories=riesgo.CLASES))
    r = riesgo.matriz_riesgo(a, v)
    assert list(r) == ["Muy alta", "Muy baja", "Baja"]


def test_quadkey_y_teselas():
    assert len(_quadkey(-69.94, -4.21, 9)) == 9
    assert _teselas_10grados((-70.15, -4.32, -69.8, -4.05)) == ["00N_070W", "00N_080W"]


def test_indice_vulnerabilidad_rango():
    m = pd.DataFrame({"densidad_construida": np.linspace(0, 1, 10), "poblacion": np.arange(10.0),
                      "dist_rio_m": np.arange(10.0)[::-1], "ndvi": np.linspace(0.2, 0.8, 10), "n_edif": np.ones(10)})
    v = riesgo.indice_vulnerabilidad(m)
    assert v.between(0, 1).all()
    assert v.iloc[-1] > v.iloc[0]
