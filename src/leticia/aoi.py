"""Área de interés: límite municipal, área urbana de análisis y malla de celdas."""
from __future__ import annotations

import geopandas as gpd
import numpy as np
from shapely.geometry import box

from .config import aoi_cfg
from .fuentes import bbox, cache, limite_municipal


def crs() -> str:
    return aoi_cfg()["crs_trabajo"]


def area_urbana() -> gpd.GeoDataFrame:
    """Extensión urbana de análisis: el rectángulo `bbox_urbano` recortado por el límite municipal."""
    mun = limite_municipal()
    geom = mun.geometry.union_all().intersection(box(*bbox("bbox_urbano")))
    return gpd.GeoDataFrame({"nombre": [aoi_cfg()["nombre"]]}, geometry=[geom], crs=4326).to_crs(crs())


def malla(tam_m: float | None = None, forzar: bool = False) -> gpd.GeoDataFrame:
    """Malla de celdas cuadradas (CRS de trabajo) que cubre el área urbana; `id` es estable entre corridas."""
    tam = tam_m or aoi_cfg()["tamano_celda_m"]

    def _crear():
        zona = area_urbana()
        x0, y0, x1, y1 = zona.total_bounds
        x0, y0 = np.floor(x0 / tam) * tam, np.floor(y0 / tam) * tam
        xs, ys = np.arange(x0, x1, tam), np.arange(y0, y1, tam)
        celdas = [box(x, y, x + tam, y + tam) for y in ys for x in xs]
        ids = [f"{int(x // tam)}_{int(y // tam)}" for y in ys for x in xs]
        g = gpd.GeoDataFrame({"id": ids}, geometry=celdas, crs=crs())
        g = g[g.intersects(zona.geometry.iloc[0])].copy()
        g["geometry"] = g.geometry.intersection(zona.geometry.iloc[0])
        g = g[g.area > 0.05 * tam * tam]
        return g.set_index("id")

    g = cache(f"malla_{int(tam)}m.parquet", _crear, forzar)
    return g.set_index("id") if "id" in g.columns else g
