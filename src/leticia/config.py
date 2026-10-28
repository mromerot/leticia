"""Configuración y rutas del proyecto.

La configuración viaja dentro del paquete (`leticia/config/*.yaml`), de modo que los cuadernos
funcionan igual en Colab (instalando el paquete desde GitHub) y en un clon local. Si la carpeta de
trabajo tiene su propio `config/aoi.yaml`, ese archivo tiene prioridad: así se replica el proyecto
en otra ciudad sin tocar el código.
"""
from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path

import yaml

_PAQUETE = Path(__file__).resolve().parent


def en_colab() -> bool:
    return "google.colab" in sys.modules


def raiz_proyecto() -> Path:
    """Raíz del proyecto: LETICIA_ROOT, la carpeta con `myst.yml` más cercana o el directorio actual."""
    env = os.environ.get("LETICIA_ROOT")
    if env:
        return Path(env).resolve()
    aqui = Path.cwd().resolve()
    for p in [aqui, *aqui.parents]:
        if (p / "myst.yml").exists() and (p / "src" / "leticia").exists():
            return p
    return aqui


def dir_config() -> Path:
    local = raiz_proyecto() / "config"
    return local if (local / "aoi.yaml").exists() else _PAQUETE / "config"


def dir_datos() -> Path:
    """Carpeta de datos descargados y procesados (no se versiona)."""
    env = os.environ.get("LETICIA_DATOS")
    if env:
        p = Path(env)
    elif en_colab():
        p = Path("/content/datos_leticia")
    else:
        p = raiz_proyecto() / "data"
    for sub in ("raw", "processed"):
        (p / sub).mkdir(parents=True, exist_ok=True)
    return p


def _leer(nombre: str) -> dict:
    with open(dir_config() / nombre, encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache
def aoi_cfg() -> dict:
    return _leer("aoi.yaml")


@lru_cache
def fuentes() -> dict:
    return _leer("sources.yaml")["capas"]


@lru_cache
def parametros() -> dict:
    return _leer("parametros.yaml")


def recargar() -> None:
    for f in (aoi_cfg, fuentes, parametros):
        f.cache_clear()
