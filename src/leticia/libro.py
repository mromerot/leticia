"""Utilidades para los cuadernos del libro (Colab o local)."""
from __future__ import annotations

import logging
import warnings

import pandas as pd

from .config import dir_datos, en_colab, recargar

REPO = "mromerot/leticia"
RAMA = "main"


def preparar(nivel_log: int = logging.WARNING) -> None:
    """Registro, avisos, formato de tablas y estilo de gráficas comunes a todos los cuadernos."""
    from . import viz

    recargar()
    logging.basicConfig(level=nivel_log, format="%(levelname)s %(name)s: %(message)s", force=True)
    for ruidoso in ("rasterio", "rasterio._err", "rasterio._env", "matplotlib", "odc", "distributed"):
        logging.getLogger(ruidoso).setLevel(logging.ERROR)
    for categoria in (FutureWarning, DeprecationWarning, RuntimeWarning, UserWarning):
        warnings.filterwarnings("ignore", category=categoria)
    pd.set_option("display.float_format", lambda v: f"{v:,.2f}")
    pd.set_option("display.max_columns", 30)
    pd.set_option("display.width", 140)
    viz.estilo()
    dir_datos()


def intentar(fn, *a, mensaje: str = "", **kw):
    """Ejecuta `fn`; si falla (servicio caído, sin red), muestra un aviso en vez de romper el cuaderno."""
    try:
        return fn(*a, **kw)
    except Exception as e:  # noqa: BLE001
        from IPython.display import Markdown, display

        display(Markdown(f":::{{warning}}\n{mensaje or 'Dato no disponible'}: `{type(e).__name__}: {str(e)[:300]}`\n:::"))
        return None


def insignia_colab(ruta_cuaderno: str) -> str:
    u = f"https://colab.research.google.com/github/{REPO}/blob/{RAMA}/{ruta_cuaderno}"
    return f"[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({u})"


def entorno() -> str:
    return "Google Colab" if en_colab() else "local"
