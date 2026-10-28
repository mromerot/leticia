"""Modelos estadísticos simples de pronóstico estacional con validación cruzada (incendios, dengue)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def media_meses(indice: pd.Series, meses: list[int]) -> pd.Series:
    """Promedio anual de un índice mensual en los meses dados (p. ej. TNA de marzo–mayo); solo años completos."""
    sel = indice[indice.index.month.isin(meses)].dropna()
    g = sel.groupby(sel.index.year)
    return g.mean()[g.size() == len(meses)]


def regresion_validada(y: pd.Series, X: pd.DataFrame, grupos: pd.Series | None = None) -> tuple[pd.Series, np.ndarray]:
    """Regresión lineal con validación cruzada que deja fuera un grupo cada vez (por defecto, cada fila).

    Devuelve las predicciones fuera de muestra y los coeficientes ajustados con todos los datos (la constante
    primero). Con `X` sin columnas el modelo es la media, que sirve de referencia («climatología»).
    """
    df = pd.concat([y.rename("_y"), X], axis=1).dropna()
    yv = df["_y"].to_numpy(float)
    A = np.column_stack([np.ones(len(df))] + [df[c].to_numpy(float) for c in X.columns])
    g = df.index.to_numpy() if grupos is None else grupos.reindex(df.index).to_numpy()
    pred = np.full(len(df), np.nan)
    for k in pd.unique(g):
        fuera = g == k
        coef, *_ = np.linalg.lstsq(A[~fuera], yv[~fuera], rcond=None)
        pred[fuera] = A[fuera] @ coef
    coef, *_ = np.linalg.lstsq(A, yv, rcond=None)
    return pd.Series(pred, index=df.index), coef


def habilidad(obs: pd.Series, pred: pd.Series, referencia: pd.Series) -> dict:
    """Correlación de Pearson, error cuadrático medio (ECM) y habilidad frente a una referencia: 1 − ECM/ECM_ref.

    Una habilidad positiva indica que el modelo mejora a la referencia (p. ej., la climatología validada igual).
    """
    df = pd.concat({"o": obs, "p": pred, "r": referencia}, axis=1).dropna()
    ecm = float(((df["o"] - df["p"]) ** 2).mean())
    ecm_ref = float(((df["o"] - df["r"]) ** 2).mean())
    return {"r": float(np.corrcoef(df["o"], df["p"])[0, 1]), "ecm": ecm, "habilidad": 1 - ecm / ecm_ref, "n": len(df)}


def prediccion_con_intervalo(coef: np.ndarray, x: list[float], residuos: pd.Series, nivel: float = 0.9) -> tuple[float, float, float]:
    """Predicción puntual y un intervalo empírico a partir de los cuantiles de los residuos de la validación cruzada."""
    centro = float(coef[0] + np.dot(coef[1:], x))
    r = residuos.dropna()
    return centro, centro + float(np.quantile(r, (1 - nivel) / 2)), centro + float(np.quantile(r, 1 - (1 - nivel) / 2))
