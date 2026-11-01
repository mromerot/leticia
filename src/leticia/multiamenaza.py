"""Análisis multiamenaza (3.9): combinación de amenazas por detonante y curvas de riesgo con bandas.

Adapta la metodología de Chen et al. (2016): las amenazas que comparten un detonante se combinan **con el máximo por
elemento** (no con la suma), los detonantes independientes se suman en la pérdida anual esperada, y cada ingrediente
incierto se calcula en una versión mínima, media y máxima.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import riesgo
from .config import parametros

BANDAS = ("minimo", "medio", "maximo")


def p_multi() -> dict:
    return parametros()["multiamenaza"]


def valor_banda(clave: str, banda: str):
    """Valor mínimo, medio o máximo de un parámetro de `multiamenaza` (lista de tres)."""
    return p_multi()[clave][BANDAS.index(banda)]


def combinar_maximo(*fracciones) -> np.ndarray:
    """Fracción de pérdida de cada elemento cuando varias amenazas del mismo detonante lo alcanzan: el máximo.

    Un edificio que se inunda y además pierde su orilla en la misma creciente no pierde dos veces su valor.
    """
    return np.maximum.reduce([np.asarray(f, dtype=float) for f in fracciones])


def combinar_suma_acotada(*fracciones) -> np.ndarray:
    """Suma de las fracciones con tope en 1: lo que resultaría de tratar las amenazas como eventos separados."""
    return np.minimum(np.sum([np.asarray(f, dtype=float) for f in fracciones], axis=0), 1.0)


def fraccion_danio_banda(profundidad_m, banda: str = "medio") -> np.ndarray:
    """Fracción de daño por profundidad (curva de Huizinga) multiplicada por el factor de la banda, con tope en 1."""
    return np.minimum(riesgo.fraccion_danio(profundidad_m) * valor_banda("factor_curva_danio", banda), 1.0)


def profundidad_encharcamiento(prof_depresion_m, periodo: int, banda: str = "medio") -> np.ndarray:
    """Profundidad del agua en cada depresión topográfica para una lluvia de periodo de retorno `periodo`."""
    c = p_multi()["lluvia"]
    llenado = np.interp(periodo, c["periodos"], c["llenado_depresion"])
    factor = c["factor_llenado"][BANDAS.index(banda)]
    return np.asarray(prof_depresion_m, dtype=float) * min(llenado * factor, 1.0)


def exposicion_por_periodo(prof_por_periodo: dict[int, np.ndarray], personas: np.ndarray, minima_m: float) -> pd.Series:
    """Personas cuya edificación tiene al menos `minima_m` de agua, para cada periodo de retorno."""
    return pd.Series({t: float(personas[np.asarray(p) >= minima_m].sum()) for t, p in prof_por_periodo.items()}).sort_index()


def razon_suma_maximo(f_a, f_b, valores) -> float:
    """Cuánto sobrestima la pérdida tratar dos amenazas como aditivas (suma acotada) frente al máximo."""
    valores = np.asarray(valores, dtype=float)
    maximo = (combinar_maximo(f_a, f_b) * valores).sum()
    return float((combinar_suma_acotada(f_a, f_b) * valores).sum() / maximo) if maximo else np.nan


def bandas_pae(curvas: dict[str, pd.Series]) -> pd.Series:
    """Pérdida anual esperada de cada banda (mínima, media, máxima) a partir de su curva pérdida–periodo de retorno."""
    return pd.Series({b: riesgo.perdida_anual_esperada(c) for b, c in curvas.items()})[list(BANDAS)]


def curva_excedencia_empirica(serie: pd.Series) -> pd.DataFrame:
    """Probabilidad anual de excedencia empírica (Weibull) de una serie anual de pérdidas o días."""
    x = serie.dropna().sort_values(ascending=False)
    n = len(x)
    return pd.DataFrame({"valor": x.values, "prob_excedencia": np.arange(1, n + 1) / (n + 1)}, index=x.index)


def pae_empirica(serie: pd.Series) -> float:
    """Valor anual esperado de una serie anual: su media (años sin evento cuentan como cero)."""
    return float(serie.dropna().mean())


def oni_pico(oni: pd.Series) -> pd.Series:
    """ONI del trimestre diciembre–febrero (el pico del ENSO) de cada año, que precede a la temporada de aguas bajas."""
    d = oni[oni.index.month == 1]
    return pd.Series(d.values, index=d.index.year, name="oni_djf")


def fase_enso(oni: pd.Series, umbral: float = 0.5) -> pd.Series:
    """Fase ENSO de cada año según el ONI de diciembre a febrero: El Niño, La Niña o neutro."""
    return pd.cut(oni_pico(oni), [-np.inf, -umbral, umbral, np.inf], labels=["La Niña", "neutro", "El Niño"])


def anual_empirico_vendaval(eventos: pd.DataFrame, valor_vivienda: float, fraccion_averiada: float,
                            anios: range) -> pd.Series:
    """Pérdida anual por vendavales registrados (viviendas averiadas y destruidas × valor medio de una vivienda)."""
    d = eventos.assign(perdida=(eventos["averiadas"].fillna(0) * fraccion_averiada + eventos["destruidas"].fillna(0)) * valor_vivienda)
    return d.groupby(d.index.year)["perdida"].sum().reindex(list(anios), fill_value=0.0)
