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
* - **Tasas de erosión y acreción de orillas por tramo de río** (`erosion_real`)
  - global
  - Langhorst y Pavelsky (2023) – Riverbank Erosion and Accretion from Landsat (REAL): REAL v0.1: tasas medias y máximas (m/año) por tramo de SWORD, Landsat 2000–2020 ([enlace](https://doi.org/10.5281/zenodo.7045021))
  - tramos de ~10 km de ríos de más de 150 m de ancho
  - CC BY 4.0
  - 2026-10-28
* - **Puntos de calor diarios en la Amazonia colombiana (2000–presente), con figura territorial** (`siatac_puntos_calor`)
  - nacional
  - Instituto SINCHI – SIAT-AC (a partir de NASA FIRMS): Puntos de calor por región (histórico), MODIS y VIIRS (S-NPP, NOAA-20, NOAA-21) ([enlace](https://datos.siatac.co/datasets/sinchi::puntos-de-calor-por-región-histórico-escala-1100-000-2))
  - 375 m – 1 km; actualización diaria
  - CC BY 4.0
  - 2026-10-30
* - **Cicatrices de quema (área quemada) en la Amazonia colombiana** (`siatac_cicatrices`)
  - nacional
  - Instituto SINCHI – SIAT-AC: Cicatrices de quema por región (histórico), escala 1:100.000 ([enlace](https://datos.siatac.co/datasets/sinchi::cicatrices-de-quema-por-región-histórico-escala-1100-000))
  - 1:100.000
  - CC BY 4.0
  - 2026-10-30
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
* - **Coberturas de la tierra (Corine Land Cover adaptada a Colombia) por año, 2002–2024** (`siatac_coberturas`)
  - nacional
  - Instituto SINCHI – SIAT-AC: Capa de coberturas de la tierra de la Amazonia colombiana, escala 1:100.000 (leyenda completa hasta 2022; agrupada en 2024) ([enlace](https://siatac.co/coberturas-100k/))
  - 1:100.000
  - CC BY 4.0 (la capa de 2023 no es dato abierto y no se usa)
  - 2026-10-30
* - **Áreas prioritarias de restauración en rondas hídricas (planicie aluvial y drenajes)** (`siatac_restauracion_rondas`)
  - nacional
  - Instituto SINCHI – SIAT-AC: Áreas prioritarias de restauración en rondas hídricas por región (2024), escala 1:100.000 ([enlace](https://datos.siatac.co/datasets/sinchi::áreas-prioritarias-de-restauración-en-rondas-hídricas-por-región-2024-escala-1100-000))
  - 1:100.000
  - CC BY 4.0
  - 2026-10-30
* - **Ecosistemas terrestres y acuáticos (aguas blancas y negras)** (`siatac_ecosistemas`)
  - nacional
  - Instituto SINCHI – SIAT-AC: Ecosistemas por región (2024), escala 1:100.000 ([enlace](https://datos.siatac.co/datasets/sinchi::ecosistemas-por-región-2024-escala-1100-000))
  - 1:100.000
  - CC BY 4.0
  - 2026-10-30
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
* - **Serie horaria de temperatura, punto de rocío, humedad y viento (1979–presente) para el estrés térmico (UTCI)** (`clima_horario`)
  - global
  - ECMWF ERA5 (vía Open-Meteo): Reanálisis ERA5 horario, celda 0,25° ([enlace](https://open-meteo.com/en/docs/historical-weather-api))
  - ~28 km, horaria
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
* - **Índice del Atlántico Norte tropical (TNA)** (`indice_tna`)
  - global
  - NOAA Physical Sciences Laboratory: TNA mensual (HadISST1.1, climatología 1991–2020), 1948–presente ([enlace](https://psl.noaa.gov/data/timeseries/month/))
  - Atlántico Norte tropical (5,5–23,5° N; 15–57,5° O)
  - Dominio público
  - 2026-10-28
* - **Casos semanales de dengue notificados por municipio (2007–2022)** (`dengue_opendengue`)
  - global
  - OpenDengue (Clarke et al., 2024) con datos del SIVIGILA – Instituto Nacional de Salud: OpenDengue V1.3, extracto espacial (Colombia a nivel municipal, semanal) ([enlace](https://doi.org/10.6084/m9.figshare.24259573))
  - municipal, semanal
  - CC BY 4.0
  - 2026-10-28
* - **Catálogo nacional de estaciones del IDEAM** (`estaciones_ideam`)
  - nacional
  - IDEAM: Catálogo Nacional de Estaciones ([enlace](https://www.datos.gov.co/resource/hp9r-jxuu.json))
  - punto
  - Datos abiertos
  - 2026-10-28
```
