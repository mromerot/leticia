"""Indicadores de amenaza por celda para la síntesis multiamenaza (3.7).

Reúne en una sola tabla los indicadores que cada flujo de la Sección 3 calcula por separado, a partir de las
mismas fuentes en caché, para que la síntesis pueda ejecutarse sola (por ejemplo, en Colab).
"""
from __future__ import annotations

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from . import aoi, espacial, exposicion, fuentes
from .config import parametros
from .fuentes import cache


def indicadores_celda(forzar: bool = False) -> gpd.GeoDataFrame:
    def _crear():
        p = parametros()
        m = exposicion.malla_exposicion().copy()
        # Inundación fluvial: profundidad de 100 años (JRC) y altura sobre el agua permanente
        dem = fuentes.raster_estatico("cop-dem-glo-30", "data")
        occ = fuentes.raster_estatico("jrc-gsw", "occurrence")
        hand = espacial.altura_sobre_agua(dem, occ >= 90)
        m["prof_rp100_m"] = espacial.estadistica_zonal(fuentes.inundacion_jrc(100).fillna(0), m, "max")
        m["hand_m"] = espacial.estadistica_zonal(hand, m)
        # Erosión: distancia a la orilla de aguas bajas más reciente
        anio = p["erosion"]["anios_comparacion"][-1]
        ds = espacial.compuesto_landsat(anio, p["erosion"]["meses_aguas_bajas"])
        agua = (espacial.mndwi(ds) > p["erosion"]["umbral_mndwi"]).rio.write_crs(4326)
        orilla = espacial.vectorizar(agua, 200).to_crs(aoi.crs()).boundary.union_all()
        m["dist_orilla_m"] = m.geometry.centroid.distance(orilla)
        # Calor: temperatura de superficie y vegetación
        lst = espacial.temperatura_superficie(2024, p["calor"]["meses_landsat"], nubes_max=p["calor"]["nubes_max"])
        m["lst_c"] = espacial.estadistica_zonal(lst["lst"].rio.write_crs(4326), m)
        m["ndvi"] = espacial.estadistica_zonal(lst["ndvi"].rio.write_crs(4326), m)
        # Incendio: distancia al foco VIIRS más cercano (2012–2025)
        f = fuentes.focos_calor("viirs-snpp", list(range(2012, 2026)))
        f = f[f["confidence"].astype(str).str.lower().isin(p["incendios"]["confianza_viirs"])]
        if len(f):
            pts = gpd.GeoSeries(gpd.points_from_xy(f.longitude, f.latitude), crs=4326).to_crs(aoi.crs())
            arbol = cKDTree(np.column_stack([pts.x, pts.y]))
            c = m.geometry.centroid
            m["dist_foco_m"] = arbol.query(np.column_stack([c.x, c.y]))[0]
        else:
            m["dist_foco_m"] = np.inf
        # Encharcamiento: profundidad media de depresiones topográficas ≥ 0,5 m
        b = fuentes.bbox("bbox_urbano", 0.01)
        prof = espacial.profundidad_depresiones(dem.sel(x=slice(b[0], b[2]), y=slice(b[3], b[1])))
        m["prof_depresion_m"] = espacial.estadistica_zonal(prof.where(prof >= 0.5, 0), m)
        return m

    g = cache("indicadores_celda.parquet", _crear, forzar)
    return g.set_index("id") if "id" in g.columns else g


def tabla_eventos() -> pd.DataFrame:
    """Une DesInventar (hasta 2018) y la UNGRD (2019–) en categorías comparables."""
    di = fuentes.desinventar()
    un = fuentes.emergencias_ungrd()
    a = di[di.index.year < 2019].assign(fuente="DesInventar")[["evento", "afectados", "vivdest", "vivafec", "fuente"]]
    a = a.rename(columns={"vivdest": "viviendas_destruidas", "vivafec": "viviendas_averiadas"})
    b = un.assign(fuente="UNGRD").rename(columns={"personas": "afectados"})[["evento", "afectados", "viviendas_destruidas", "viviendas_averiadas", "fuente"]]
    t = pd.concat([a, b]).sort_index()
    t["categoria"] = t["evento"].map(categoria_evento)
    return t


def categoria_evento(e: str) -> str:
    e = str(e).upper()
    if "INUND" in e or "CRECIENTE" in e or "AVENIDA" in e:
        return "Inundación"
    if "SEQU" in e or "DESABAST" in e or "ESTIAJE" in e:
        return "Sequía y desabastecimiento"
    if "EROS" in e or "DESLIZ" in e or "MOVIMIENTO EN MASA" in e or "SOCAV" in e:
        return "Erosión y movimientos en masa"
    if "FOREST" in e or "COBERTURA VEGETAL" in e:
        return "Incendio de cobertura vegetal"
    if "INCENDIO" in e:
        return "Incendio estructural"
    if "VENDAVAL" in e or "LLUVIA" in e or "TORMENTA" in e or "GRANIZ" in e or "ELÉCTRICA" in e or "ELECTRICA" in e:
        return "Vendaval y lluvias"
    if "NAUFRAG" in e or "FLUVIAL" in e or "MARITIMO" in e or "AÉREO" in e or "AEREO" in e or "ACCIDENTE" in e:
        return "Accidentes de transporte"
    return "Otros"
