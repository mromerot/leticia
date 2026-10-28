---
title: 2.4 Otros datos
short_title: 2.4 Otros
---

- **Imágenes Landsat 5, 7, 8 y 9 (Collection 2, Level-2)**, desde Microsoft Planetary Computer: compuestos de aguas
  bajas para el cauce (1987–2024) y temperatura de superficie (banda térmica de Landsat 8/9). El agua se detecta con
  el índice MNDWI [@xu2006mndwi].
- **Sentinel-2 L2A**: mosaico en color verdadero de las escenas más despejadas de 2023–2025, usado como mapa base.
- **Índice Oceánico El Niño (ONI)** del Centro de Predicción Climática de la NOAA, para relacionar las vaciantes con
  El Niño.
- **Índice del Atlántico Norte tropical (TNA)** del Laboratorio de Ciencias Físicas de la NOAA [@noaa2026tna]: la
  temperatura del mar que más influye en la temporada seca del occidente amazónico, usada para anticipar la
  temporada de incendios [@fernandes2011] y como predictor del dengue.
- **Casos de dengue** notificados al SIVIGILA del Instituto Nacional de Salud, por semana epidemiológica y municipio
  (2007–2022), tal como los compila y estandariza **OpenDengue** [@clarke2024opendengue].
- **Catálogo Nacional de Estaciones del IDEAM** (Datos Abiertos), para ubicar las estaciones de Leticia: LETICIA
  [48017010] (nivel), NAZARETH [48017030] (nivel) y AEROPUERTO VÁSQUEZ COBO [48015050] (sinóptica).

## Métodos estadísticos

- **Extremos**: distribución generalizada de valores extremos (GEV) ajustada por L-momentos, más estable que la
  máxima verosimilitud con muestras cortas o con valores atípicos como la vaciante de 2024 [@hosking1985;
  @coles2001extremes]; intervalos de confianza por remuestreo.
- **Tendencias**: prueba de Mann-Kendall y pendiente de Sen [@mann1945; @sen1968].
- **Sequía**: SPI con ajuste gamma [@mckee1993] y SPEI con ajuste log-logístico del balance lluvia − evapotranspiración
  [@vicente2010spei], contrastado con el paquete `SPEI` de Python [@vonk2026spei].
- **Calor**: umbrales relativos (percentil 90 de 1991–2020), temperatura aparente de Steadman [@steadman1984] y
  UTCI con la implementación del ECMWF [@brode2012utci; @brimicombe2022thermofeel].
- **Aguas bajas**: días por año hidrológico bajo el P80 de la curva de duración [@santosdelima2024].
- **Pronósticos estacionales**: regresiones lineales validadas dejando fuera un año cada vez, comparadas con la
  climatología; incendios con el TNA [@fernandes2011] y dengue a 1, 3 y 6 meses [@beal2025dengue].
- **Altura sobre el río**: aproximación al descriptor HAND [@renno2008hand].
