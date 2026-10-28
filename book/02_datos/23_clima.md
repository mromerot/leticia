---
title: 2.3 Datos de clima
short_title: 2.3 Clima
---

## Clima observado: ERA5

La serie diaria de temperatura máxima y mínima, temperatura aparente, humedad, punto de rocío, lluvia, viento,
rachas y evapotranspiración de referencia proviene del reanálisis **ERA5** del ECMWF (1950–presente, celda de
0,25°) [@hersbach2020], consultado con la API histórica de Open-Meteo [@zippenfenig2023openmeteo].

:::{important} Limitaciones de ERA5 en Leticia
Una celda de ~28 km dominada por bosque y río **subestima** el calor de la ciudad construida, la lluvia de los
aguaceros convectivos y las rachas de los vendavales. Para tendencias y anomalías es adecuada; para diseño de obras
se necesitan las series de la estación sinóptica del aeropuerto Vásquez Cobo [48015050] del IDEAM. Antes de 1979
(era presatelital) la lluvia de ERA5 es menos confiable y los índices de sequía se calculan desde 1979.
:::

## Proyecciones: CCKP del Banco Mundial (CMIP6)

El **Climate Change Knowledge Portal** publica en un repositorio público el ensamble CMIP6 de 25 modelos con
reducción de escala NEX-GDDP-CMIP6 a 0,25°, para cinco escenarios SSP y decenas de índices [@cckp2024;
@thrasher2022]. El paquete lee la celda de Leticia por peticiones de rango HTTP (sin descargar los archivos
globales) y guarda los valores en caché.

```{list-table} Índices del CCKP usados
:header-rows: 1
* - Código
  - Índice
  - Flujo
* - tas, tasmax, txx
  - Temperatura media, máxima media y máxima absoluta anual
  - 3.2, 3.4, 3.5
* - hd35, hi35, tr26
  - Días con Tmax > 35 °C, días con índice de calor > 35 °C, noches con Tmin > 26 °C
  - 3.4
* - pr, rx1day, rx5day, r20mm
  - Lluvia anual, máxima en 1 y 5 días, días con lluvia ≥ 20 mm
  - 3.1, 3.6
* - cdd, spei12
  - Días secos consecutivos y SPEI de 12 meses
  - 3.2, 3.5
```
