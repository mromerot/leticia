"""Exposición: edificaciones y población en la malla de análisis."""
from __future__ import annotations

import geopandas as gpd
import numpy as np
import pandas as pd

from . import aoi, fuentes
from .fuentes import cache


def edificaciones_urbanas() -> gpd.GeoDataFrame:
    """Huellas de edificaciones dentro del área urbana de Leticia (sin Tabatinga), con área y población asignada."""

    def _crear():
        e = fuentes.edificaciones().to_crs(aoi.crs())
        zona = aoi.area_urbana().geometry.iloc[0]
        e = e[e.representative_point().within(zona)].copy()
        e["area_m2"] = e.area
        e = e[e["area_m2"] >= 12].reset_index(drop=True)
        e["poblacion"] = _poblacion_dasimetrica(e)
        e["id_celda"] = _celda_de(e)
        return e

    return cache("edificaciones_urbanas.parquet", _crear)


def _poblacion_dasimetrica(e: gpd.GeoDataFrame) -> np.ndarray:
    """Reparte la población de cada hexágono de Kontur entre sus edificaciones, en proporción al área de la huella."""
    hexes = fuentes.poblacion().to_crs(e.crs)
    # Los hexágonos de la frontera mezclan población de Tabatinga (Brasil): se conserva solo la fracción
    # del hexágono que cae dentro del municipio.
    mun = fuentes.limite_municipal().to_crs(e.crs).geometry.union_all()
    hexes["population"] = hexes["population"] * (hexes.geometry.intersection(mun).area / hexes.area)
    pts = gpd.GeoDataFrame(geometry=e.representative_point(), crs=e.crs)
    j = gpd.sjoin(pts, hexes[["h3", "population", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated()]
    area = e["area_m2"].values
    area_hex = pd.Series(area, index=e.index).groupby(j["h3"]).transform("sum")
    return (j["population"].fillna(0) * area / area_hex.replace(0, np.nan)).fillna(0).values


def _celda_de(e: gpd.GeoDataFrame) -> pd.Series:
    m = aoi.malla()
    pts = gpd.GeoDataFrame(geometry=e.representative_point(), crs=e.crs)
    j = gpd.sjoin(pts, m.reset_index()[["id", "geometry"]], how="left", predicate="within")
    return j[~j.index.duplicated()]["id"].values


def malla_exposicion() -> gpd.GeoDataFrame:
    """Malla con número de edificaciones, área construida y población estimada por celda."""

    def _crear():
        m = aoi.malla().copy()
        e = edificaciones_urbanas()
        g = e.groupby("id_celda")
        m["n_edif"] = g.size().reindex(m.index).fillna(0).astype(int)
        m["area_edif_m2"] = g["area_m2"].sum().reindex(m.index).fillna(0)
        m["poblacion"] = g["poblacion"].sum().reindex(m.index).fillna(0)
        m["densidad_construida"] = m["area_edif_m2"] / m.area
        return m

    return cache("malla_exposicion.parquet", _crear)


def asentamientos_rurales(clave_bbox: str = "bbox_ribera", poblacion_minima: float = 10) -> gpd.GeoDataFrame:
    """Hexágonos de Kontur con población dentro del municipio y fuera del casco urbano, como puntos (centroides).

    Aproximan las comunidades ribereñas y rurales cuando no hay una capa pública de asentamientos. La población de
    cada hexágono se reduce a la fracción que cae dentro del municipio.
    """
    hexes = fuentes.poblacion(clave_bbox).to_crs(aoi.crs())
    mun = fuentes.limite_municipal().to_crs(aoi.crs()).geometry.union_all()
    urbana = aoi.area_urbana().geometry.iloc[0]
    hexes["poblacion"] = hexes["population"] * hexes.geometry.intersection(mun).area / hexes.area
    hexes = hexes[(hexes["poblacion"] >= poblacion_minima) & ~hexes.intersects(urbana)]
    return gpd.GeoDataFrame(hexes[["h3", "poblacion"]].reset_index(drop=True), geometry=hexes.geometry.centroid.values, crs=hexes.crs)


def resumen(m: gpd.GeoDataFrame) -> pd.Series:
    return pd.Series({"celdas": len(m), "celdas con edificaciones": int((m["n_edif"] > 0).sum()),
                      "edificaciones": int(m["n_edif"].sum()), "área construida (ha)": m["area_edif_m2"].sum() / 1e4,
                      "población estimada": m["poblacion"].sum()})
