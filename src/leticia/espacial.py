"""Procesamiento espacial: compuestos satelitales, índices de agua, altura sobre el río y estadística zonal."""
from __future__ import annotations

import logging

import geopandas as gpd
import numpy as np
import pandas as pd
import rioxarray  # noqa: F401  (registra el accesorio .rio)
import xarray as xr
from rasterio import features
from scipy import ndimage

from .config import parametros
from .fuentes import bbox, cache, catalogo_pc

log = logging.getLogger(__name__)

# Bits de QA_PIXEL de Landsat C2: relleno, nube dilatada, cirro, nube, sombra
_BITS_MALOS = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4)


def xy(obj):
    """odc-stac nombra latitude/longitude en EPSG:4326; rioxarray y el resto del paquete usan x/y."""
    ren = {k: v for k, v in (("latitude", "y"), ("longitude", "x")) if k in obj.dims}
    obj = obj.rename(ren) if ren else obj
    return obj.rio.write_crs(4326) if obj.rio.crs is None else obj


def _landsat_items(b, inicio: str, fin: str, nubes_max: float, meses: list[int] | None = None):
    items = catalogo_pc().search(collections=["landsat-c2-l2"], bbox=b, datetime=f"{inicio}/{fin}",
                                 query={"eo:cloud_cover": {"lt": nubes_max}}).item_collection()
    items = [i for i in items if i.properties.get("platform") in ("landsat-5", "landsat-7", "landsat-8", "landsat-9")]
    if meses:
        items = [i for i in items if pd.Timestamp(i.datetime).month in meses]
    return items


def compuesto_landsat(anio: int, meses: list[int], clave_bbox: str = "bbox_regional", nubes_max: float = 70,
                      bandas=("green", "swir16", "nir08", "red"), resolucion: float = 0.0003, ventana_anios: int = 0,
                      forzar: bool = False) -> xr.Dataset:
    """Mediana de reflectancia de superficie Landsat en los meses dados (nubes y sombras enmascaradas).

    `ventana_anios` amplía la búsqueda a ±n años cuando un solo año no tiene escenas suficientes.
    """
    import odc.stac

    b = bbox(clave_bbox)
    nombre = f"landsat_{anio}_{'-'.join(map(str, meses))}_{clave_bbox}_{'-'.join(bandas)}.nc"

    def _crear():
        items = _landsat_items(b, f"{anio - ventana_anios}-01-01", f"{anio + ventana_anios}-12-31", nubes_max, meses)
        if not items:
            raise LookupError(f"Sin escenas Landsat para {anio} (meses {meses})")
        ds = odc.stac.load(items, bands=list(bandas) + ["qa_pixel"], bbox=b, crs="EPSG:4326", resolution=resolucion,
                           groupby="solar_day", chunks={"x": 1024, "y": 1024})
        ds = xy(ds)
        malo = (ds["qa_pixel"].astype("uint16") & _BITS_MALOS) > 0
        out = {}
        for banda in bandas:
            v = ds[banda].where(~malo & (ds[banda] > 0)) * 0.0000275 - 0.2
            out[banda] = v.median("time").compute()
        res = xr.Dataset(out)
        res.attrs.update(escenas=len(items), plataformas=",".join(sorted({i.properties["platform"] for i in items})))
        res["validas"] = (~malo).sum("time").compute().astype("int16")
        return res

    p = cache_nc(nombre, _crear, forzar)
    return p


def cache_nc(nombre: str, fn, forzar: bool = False) -> xr.Dataset:
    from .fuentes import ruta

    p = ruta(nombre)
    if p.exists() and not forzar:
        return xr.open_dataset(p).load()
    ds = fn()
    ds.to_netcdf(p)
    return ds


def mndwi(ds: xr.Dataset) -> xr.DataArray:
    """Índice de agua normalizado modificado (Xu 2006): (verde − SWIR1)/(verde + SWIR1)."""
    return (ds["green"] - ds["swir16"]) / (ds["green"] + ds["swir16"])


def ndvi(ds: xr.Dataset) -> xr.DataArray:
    return (ds["nir08"] - ds["red"]) / (ds["nir08"] + ds["red"])


def temperatura_superficie(anio: int, meses: list[int], clave_bbox: str = "bbox_urbano", nubes_max: float = 60,
                           anios_ventana: int = 2, forzar: bool = False) -> xr.Dataset:
    """Mediana de temperatura de superficie (°C) Landsat 8/9 y NDVI en una ventana de años y meses."""
    import odc.stac

    b = bbox(clave_bbox, 0.005)
    nombre = f"lst_{anio}_{'-'.join(map(str, meses))}_{clave_bbox}.nc"

    def _crear():
        items = _landsat_items(b, f"{anio - anios_ventana}-01-01", f"{anio}-12-31", nubes_max, meses)
        items = [i for i in items if i.properties["platform"] in ("landsat-8", "landsat-9")]
        ds = odc.stac.load(items, bands=["lwir11", "red", "nir08", "qa_pixel"], bbox=b, crs="EPSG:4326",
                           resolution=0.00027, groupby="solar_day")
        ds = xy(ds)
        malo = (ds["qa_pixel"].astype("uint16") & _BITS_MALOS) > 0
        lst = (ds["lwir11"].where(~malo & (ds["lwir11"] > 0)) * 0.00341802 + 149.0 - 273.15)
        red = ds["red"].where(~malo & (ds["red"] > 0)) * 0.0000275 - 0.2
        nir = ds["nir08"].where(~malo & (ds["nir08"] > 0)) * 0.0000275 - 0.2
        validas = lst.notnull().sum("time")
        # anomalía por escena (resta la mediana de la escena) para comparar fechas con distinto calor de fondo
        anom = lst - lst.median(["x", "y"])
        res = xr.Dataset({"lst": lst.median("time"), "lst_anomalia": anom.median("time"),
                          "ndvi": ((nir - red) / (nir + red)).median("time"), "validas": validas})
        res.attrs.update(escenas=len(items))
        return res.compute()

    return cache_nc(nombre, _crear, forzar)


def mosaico_rgb(clave_bbox: str = "bbox_regional", anios: tuple[int, int] = (2023, 2025), resolucion: float = 0.00012,
                max_escenas: int = 30, forzar: bool = False) -> xr.DataArray:
    """Mosaico Sentinel-2 en color verdadero (mediana sin nubes de las escenas más despejadas) para usar como mapa base."""
    import odc.stac

    b = bbox(clave_bbox)
    nombre = f"s2_rgb_{clave_bbox}.tif"

    def _crear():
        items = catalogo_pc().search(collections=["sentinel-2-l2a"], bbox=b, datetime=f"{anios[0]}-01-01/{anios[1]}-12-31",
                                     query={"eo:cloud_cover": {"lt": 30}}).item_collection()
        items = sorted(items, key=lambda i: i.properties["eo:cloud_cover"])[:max_escenas]
        ds = odc.stac.load(items, bands=["B04", "B03", "B02", "SCL"], bbox=b, crs="EPSG:4326", resolution=resolucion,
                           groupby="solar_day", chunks={"x": 2048, "y": 2048})
        ds = xy(ds)
        ok = ds["SCL"].isin([2, 4, 5, 6, 7, 11])
        # Desde la línea base 04.00 (2022) los niveles digitales de L2A traen un desplazamiento de +1000.
        capas = [((ds[k].where(ok & (ds[k] > 0)).astype("float32") - 1000) / 10000).median("time") for k in ("B04", "B03", "B02")]
        rgb = xr.concat(capas, dim="banda").clip(0, 1)
        rgb = (np.clip(rgb / 0.22, 0, 1) ** 0.85 * 255).fillna(0).astype("uint8").compute()
        return rgb.assign_coords(banda=[1, 2, 3]).rio.write_crs(4326)

    return cache(nombre, _crear, forzar)


def altura_sobre_agua(dem: xr.DataArray, agua: xr.DataArray) -> xr.DataArray:
    """Altura de cada píxel sobre el píxel de agua permanente más cercano (aproximación tipo HAND).

    En una llanura casi plana como la de Leticia, esta diferencia aproxima cuánto debe subir el río para
    alcanzar un lugar. No sigue la red de drenaje, así que en quebradas internas subestima la protección.
    """
    a = agua.reindex_like(dem, method="nearest").fillna(0).values.astype(bool)
    _, (iy, ix) = ndimage.distance_transform_edt(~a, return_indices=True)
    nivel_agua = dem.values[iy, ix]
    return dem.copy(data=dem.values - nivel_agua)


def profundidad_depresiones(dem: xr.DataArray) -> xr.DataArray:
    """Profundidad de las depresiones topográficas (m): diferencia entre el DEM con sumideros rellenos y el DEM.

    Las depresiones son lugares donde el agua de lluvia se acumula si el drenaje no la evacúa. Con un modelo de
    superficie (que incluye árboles y techos) aparecen depresiones falsas entre copas o edificios, por lo que se
    usa como indicador relativo y se filtran profundidades menores a 0,5 m.
    """
    from skimage.morphology import reconstruction

    z = np.nan_to_num(dem.values.astype("float64"), nan=float(np.nanmax(dem.values)))
    semilla = z.copy()
    semilla[1:-1, 1:-1] = z.max()
    lleno = reconstruction(semilla, z, method="erosion")
    return dem.copy(data=(lleno - z).astype("float32"))


def estadistica_zonal(da: xr.DataArray, celdas: gpd.GeoDataFrame, como: str = "mean") -> pd.Series:
    """Media (o suma, máximo, fracción) de un ráster en cada celda, rasterizando los polígonos en la grilla del ráster."""
    crs_r = da.rio.crs or "EPSG:4326"
    c = celdas.to_crs(crs_r)
    etiquetas = np.arange(1, len(c) + 1)
    transf = da.rio.transform()
    grilla = features.rasterize(zip(c.geometry, etiquetas), out_shape=da.shape[-2:], transform=transf, fill=0, all_touched=False)
    v = np.asarray(da.values, dtype=float)
    ok = (grilla > 0) & np.isfinite(v)
    n = np.bincount(grilla[ok], minlength=len(c) + 1)[1:]
    if como == "max":
        out = pd.Series(v[ok]).groupby(grilla[ok]).max().reindex(etiquetas)
        return pd.Series(out.values, index=celdas.index)
    suma = np.bincount(grilla[ok], weights=v[ok], minlength=len(c) + 1)[1:]
    res = suma if como == "sum" else np.where(n > 0, suma / np.maximum(n, 1), np.nan)
    return pd.Series(res, index=celdas.index)


def vectorizar(mascara: xr.DataArray, minimo_pixeles: int = 20) -> gpd.GeoDataFrame:
    """Convierte una máscara booleana en polígonos (para mapas de agua y orillas)."""
    m = mascara.fillna(0).values.astype("uint8")
    m = ndimage.binary_opening(m, iterations=1).astype("uint8")
    etiquetas, _ = ndimage.label(m)
    tam = np.bincount(etiquetas.ravel())
    m = np.where(tam[etiquetas] >= minimo_pixeles, m, 0).astype("uint8")
    geoms = [g for g, v in features.shapes(m, mask=m > 0, transform=mascara.rio.transform()) if v == 1]
    from shapely.geometry import shape

    return gpd.GeoDataFrame(geometry=[shape(g) for g in geoms], crs=mascara.rio.crs or "EPSG:4326")


def distancia_a(celdas: gpd.GeoDataFrame, objetivo: gpd.GeoDataFrame) -> pd.Series:
    """Distancia (m) del centroide de cada celda a la geometría objetivo más cercana."""
    g = objetivo.to_crs(celdas.crs).geometry.union_all()
    return celdas.geometry.centroid.distance(g)


def parametro(seccion: str, clave: str):
    return parametros()[seccion][clave]
