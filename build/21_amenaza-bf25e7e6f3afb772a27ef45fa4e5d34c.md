---
title: 2.1 Datos de amenaza
short_title: 2.1 Amenaza
---

## Nivel del río Amazonas en Leticia (IDEAM)

La pieza central del libro es la **serie diaria de nivel de la estación limnimétrica LETICIA [48017010]** del IDEAM,
instalada en 1986, con datos desde diciembre de 1987 hasta la actualidad [@ideam2026niveles]. El IDEAM publica los
niveles medios (NV_MEDIA_D), mínimos y máximos diarios en un repositorio público compatible con S3 enlazado desde
Datos Abiertos Colombia. Cada registro indica si es **definitivo** o **preliminar**. Los niveles están en
centímetros sobre el cero de la regla, no en metros sobre el nivel del mar.

:::{warning} Control de calidad
La serie publicada tiene lagunas y algunos errores. El libro descarta valores imposibles (ceros), saltos mayores a
1,2 m frente a la mediana móvil y **todo 2007**, año en que la serie queda 5–7 m por debajo de su climatología todos
los meses, señal de un cambio del cero de la regla no corregido ([3.1.b](../03_analisis/31_inundacion/b_amenaza.ipynb)).
:::

## Caudal y pronóstico (GloFAS)

El **Global Flood Awareness System** (GloFAS v4, Copernicus) simula el caudal diario de los ríos del mundo desde
1984 y emite pronósticos por ensamble [@grimaldi2022glofas]. Se consulta con la API de Open-Meteo
[@zippenfenig2023openmeteo] en la celda del cauce principal aguas arriba de Leticia (caudal medio ~40 000 m³/s).

## Mapas de inundación (JRC)

Los **mapas globales de amenaza por inundación fluvial** del JRC (v2.1) dan la profundidad del agua para periodos de
retorno de 10 a 500 años, a ~90 m, simulados con LISFLOOD-FP a partir de los caudales de GloFAS [@baugh2024jrc]. Se
leen por ventanas desde sus teselas GeoTIFF, sin descargar los archivos completos.

## Agua superficial 1984–2021 (JRC Global Surface Water)

El conjunto **Global Surface Water** clasifica cada píxel Landsat de 30 m como agua o tierra en 1984–2021 y resume
su **ocurrencia**, **estacionalidad** y **transiciones** [@pekel2016]. Se usa para ver las zonas que se inundan con
frecuencia y la migración del cauce.

## Erosión y acreción de orillas (REAL)

El conjunto **Riverbank Erosion and Accretion from Landsat** (REAL) estima la tasa media y máxima de erosión y de
acreción de la orilla (m/año) de cada tramo de unos 10 km de los ríos de más de 150 m de ancho, a partir de hasta 20
años de clasificaciones de agua de Landsat, con una estimación del ruido de cada tasa [@langhorst2023real;
@langhorst2022realdata]. El paquete descarga solo la tabla de atributos del shapefile (~130 MB) y la recorta a la
extensión regional; los tramos con islas y cauces múltiples no tienen estimación.

## Focos de calor (NASA FIRMS) y pérdida de bosque (Hansen)

Los focos de calor activos de **MODIS** (1 km, 2001–) y **VIIRS** (375 m, 2012–) se descargan del archivo anual por
país de FIRMS [@giglio2016; @schroeder2014]. Para el pronóstico de la temporada se unen los archivos de Colombia, Perú
y Brasil en la triple frontera, porque el humo que llega a Leticia se quema sobre todo fuera del municipio. Los fuegos
pequeños escapan a estos sensores, así que los conteos son un mínimo [@randerson2012]. La **pérdida anual de
cobertura arbórea** (2001–2024) proviene de Global Forest Change v1.12 [@hansen2013].

## Puntos de calor y cicatrices de quema (SINCHI, SIAT-AC)

El Sistema de Información Ambiental Territorial de la Amazonia colombiana (**SIAT-AC**) del Instituto SINCHI
publica como datos abiertos (CC BY 4.0) dos capas de fuego para la región [@sinchi2026siatac]:

- **Puntos de calor diarios** desde 2000, a partir de FIRMS, con todos los niveles de confianza y los satélites
  S-NPP, NOAA-20 y NOAA-21. Cada punto trae la figura territorial donde cae (en Leticia, resguardo indígena o área
  sustraída de la Reserva Forestal), lo que FIRMS no ofrece. Por incluir todas las detecciones, registra cerca
  del doble de puntos que los focos de FIRMS filtrados por confianza que usa el libro ([3.5.b](../03_analisis/35_incendios/b_amenaza.ipynb)).
- **Cicatrices de quema** (área quemada) cartografiadas a escala 1:100.000, con la cobertura que ardió; en la extensión de
  Leticia hay registros desde 2018.

El paquete las consulta en el servicio ArcGIS REST del SIAT-AC (`fuentes.siatac`), recortadas a la extensión
regional y en páginas de 1 000 registros.

## Registros de desastres (DesInventar y UNGRD) y tamizaje (ThinkHazard)

- **DesInventar Sendai** mantiene el inventario histórico de desastres de Colombia (fichas por municipio); para
  Leticia hay 63 registros desde 1970 [@desinventar].
- La **UNGRD** publica en Datos Abiertos el consolidado anual de emergencias desde 2019, en varios conjuntos con
  columnas distintas que el paquete armoniza [@ungrd2026emergencias].
- **ThinkHazard!** (GFDRR) da un nivel de amenaza por tipo para cada municipio del mundo [@thinkhazard2024].
