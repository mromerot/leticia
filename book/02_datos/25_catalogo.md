---
title: 2.5 Catálogo de fuentes
short_title: 2.5 Catálogo
---

Tabla generada automáticamente desde `config/sources.yaml` con `python -m leticia.catalogo`. Cada capa indica su
nivel de respaldo, la entidad responsable, el producto, la resolución, la licencia y la fecha en que se verificó
que el recurso responde desde la nube.

## 2.1 Amenaza

```{list-table}
:header-rows: 1
* - Capa
  - Nivel
  - Entidad y producto
  - Escala
  - Licencia
  - Verificado
* - **Nivel diario del río Amazonas en Leticia (medio, mínimo y máximo)** (`nivel_rio_leticia`)
  - nacional
  - IDEAM: Estación limnimétrica LETICIA [48017010], series NV_MEDIA_D, NV_MN_D y NV_MX_D ([enlace](https://www.datos.gov.co/d/9fxi-fthb))
  - puntual, diaria, 1987–presente
  - Datos abiertos (Ley 1712 de 2014)
  - 2026-10-28
* - **Caudal diario simulado del Amazonas (reanálisis y pronóstico)** (`caudal_glofas`)
  - global
  - Copernicus EMS – GloFAS v4 (vía Open-Meteo): river_discharge diario 1984–presente, celda 0,05° ([enlace](https://open-meteo.com/en/docs/flood-api))
  - ~5 km
  - CC BY 4.0
  - 2026-10-28
* - **Mapas globales de amenaza por inundación fluvial (profundidad por periodo de retorno)** (`inundacion_jrc`)
  - global
  - JRC – Copernicus EMS (GloFAS): Global river flood hazard maps v2.1 (RP10–RP500), LISFLOOD-FP ([enlace](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-GLOFAS/flood_hazard))
  - 3 arcsec (~90 m)
  - ODbL 1.0
  - 2026-10-28
* - **Agua superficial 1984–2021: ocurrencia, estacionalidad y transiciones** (`agua_superficial_jrc`)
  - global
  - JRC – Global Surface Water (Pekel et al. 2016): occurrence, seasonality, transitions, extent ([enlace](https://planetarycomputer.microsoft.com/api/stac/v1))
  - 30 m
  - Uso libre con atribución
  - 2026-10-28
* - **Imágenes Landsat 5/7/8/9 (agua, orillas y temperatura de superficie)** (`landsat`)
  - global
  - USGS / NASA (Microsoft Planetary Computer): Landsat Collection 2 Level-2 (reflectancia y temperatura de superficie) ([enlace](https://planetarycomputer.microsoft.com/api/stac/v1))
  - 30 m
  - Dominio público
  - 2026-10-28
* - **Focos de calor activos (incendios detectados por satélite)** (`focos_calor`)
  - global
  - NASA FIRMS: Archivo anual por país, MODIS (1 km, 2001–) y VIIRS S-NPP (375 m, 2012–) ([enlace](https://firms.modaps.eosdis.nasa.gov/data/country))
  - 375 m – 1 km
  - Uso libre con atribución (NASA)
  - 2026-10-28
* - **Área quemada mensual** (`area_quemada`)
  - global
  - NASA MODIS (Microsoft Planetary Computer): MCD64A1 v6.1 ([enlace](https://planetarycomputer.microsoft.com/api/stac/v1))
  - 500 m
  - Dominio público
  - 2026-10-28
* - **Pérdida anual de cobertura arbórea** (`perdida_bosque`)
  - global
  - Hansen et al. / University of Maryland – Global Forest Change: GFC v1.12 (2001–2024): treecover2000, lossyear ([enlace](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12))
  - 30 m
  - CC BY 4.0
  - 2026-10-28
* - **Emergencias reportadas a la UNGRD (2019–presente)** (`emergencias_ungrd`)
  - nacional
  - UNGRD: Consolidado de emergencias por municipio (Datos Abiertos Colombia) ([enlace](https://www.datos.gov.co/d/wwkg-r6te))
  - municipal, por evento
  - Datos abiertos
  - 2026-10-28
* - **Inventario histórico de desastres (1914–presente)** (`desinventar`)
  - nacional
  - DesInventar Sendai (Corporación OSSO / UNDRR) con registros de la UNGRD: Exportación nacional de Colombia (fichas por municipio) ([enlace](https://www.desinventar.net))
  - municipal, por evento
  - Uso libre con atribución
  - 2026-10-28
* - **Nivel de amenaza por tipo (tamizaje global)** (`thinkhazard`)
  - global
  - GFDRR – Banco Mundial: ThinkHazard! (Leticia, código 13336) ([enlace](https://thinkhazard.org/en/report/13336-colombia-amazonas-leticia.json))
  - municipal
  - CC BY 4.0 (verificar por amenaza)
  - 2026-10-28
```

## 2.2 Exposición y vulnerabilidad

```{list-table}
:header-rows: 1
* - Capa
  - Nivel
  - Entidad y producto
  - Escala
  - Licencia
  - Verificado
* - **Límite municipal de Leticia** (`limite_municipal`)
  - nacional
  - DANE (vía geoBoundaries): Marco Geoestadístico Nacional, nivel municipal (2020) ([enlace](https://www.geoboundaries.org/api/current/gbOpen/COL/ADM2/))
  - 1:100.000 (simplificado)
  - CC BY 4.0
  - 2026-10-28
* - **Huellas de edificaciones** (`edificaciones`)
  - global
  - Microsoft – Global ML Building Footprints: Huellas derivadas de imágenes (2014–2024), particionadas por quadkey ([enlace](https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv))
  - edificación
  - ODbL
  - 2026-10-28
* - **Población en hexágonos H3 de 400 m** (`poblacion`)
  - global
  - Kontur (GHSL, Facebook HRSL, Microsoft Buildings, Copernicus): Kontur Population Colombia 2023-11-01 ([enlace](https://data.humdata.org/dataset/kontur-population-colombia))
  - H3 resolución 8 (~0,7 km²)
  - CC BY 4.0
  - 2026-10-28
* - **Cobertura del suelo (incluye área construida y bosque)** (`cobertura_suelo`)
  - global
  - ESA WorldCover: WorldCover 10 m 2021 v200 ([enlace](https://planetarycomputer.microsoft.com/api/stac/v1))
  - 10 m
  - CC BY 4.0
  - 2026-10-28
* - **Modelo digital de superficie** (`elevacion`)
  - global
  - Copernicus DEM GLO-30: DSM 30 m (TanDEM-X 2011–2015) ([enlace](https://planetarycomputer.microsoft.com/api/stac/v1))
  - 30 m
  - Copernicus DEM (libre con atribución)
  - 2026-10-28
* - **Infraestructura crítica (hospital, aeropuerto, puerto, acueducto)** (`lugares_clave`)
  - global
  - OpenStreetMap (Nominatim): Geocodificación de lugares con nombre ([enlace](https://nominatim.openstreetmap.org/search))
  - punto
  - ODbL
  - 2026-10-28
```

## 2.3 Clima

```{list-table}
:header-rows: 1
* - Capa
  - Nivel
  - Entidad y producto
  - Escala
  - Licencia
  - Verificado
* - **Serie diaria de temperatura, humedad, lluvia y viento (1950–presente)** (`clima_diario`)
  - global
  - ECMWF ERA5 (vía Open-Meteo): Reanálisis ERA5, celda 0,25° ([enlace](https://open-meteo.com/en/docs/historical-weather-api))
  - ~28 km
  - CC BY 4.0
  - 2026-10-28
* - **Proyecciones CMIP6 (ensamble de modelos) de temperatura, lluvia, sequía y calor** (`proyecciones_cckp`)
  - global
  - Banco Mundial – Climate Change Knowledge Portal (CCKP): CMIP6 0,25° (reducción de escala estadística), SSP1-2.6, SSP2-4.5, SSP5-8.5 ([enlace](https://climateknowledgeportal.worldbank.org))
  - 0,25°
  - CC BY 4.0
  - 2026-10-28
```

## 2.4 Otros

```{list-table}
:header-rows: 1
* - Capa
  - Nivel
  - Entidad y producto
  - Escala
  - Licencia
  - Verificado
* - **Mosaico Sentinel-2 en color verdadero (mapa base)** (`sentinel2`)
  - global
  - ESA Copernicus (Microsoft Planetary Computer): Sentinel-2 L2A ([enlace](https://planetarycomputer.microsoft.com/api/stac/v1))
  - 10 m
  - Copernicus (libre)
  - 2026-10-28
* - **Índice Oceánico El Niño (ONI)** (`indices_oceanicos`)
  - global
  - NOAA Climate Prediction Center: ONI (ERSSTv5), trimestres móviles 1950–presente ([enlace](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt))
  - Pacífico ecuatorial (Niño 3.4)
  - Dominio público
  - 2026-10-28
* - **Catálogo nacional de estaciones del IDEAM** (`estaciones_ideam`)
  - nacional
  - IDEAM: Catálogo Nacional de Estaciones ([enlace](https://www.datos.gov.co/resource/hp9r-jxuu.json))
  - punto
  - Datos abiertos
  - 2026-10-28
```
