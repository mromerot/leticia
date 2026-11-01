---
title: 3.6.a Descripción — Lluvias intensas y vendavales
short_title: a. Descripción
---

## La amenaza en Leticia

Las tormentas convectivas de la tarde descargan en una o dos horas lluvias intensas con ráfagas fuertes y descargas
eléctricas. Los vendavales levantan techos de zinc y derriban árboles y redes; los aguaceros desbordan el drenaje en
las zonas bajas y en los cauces de las quebradas urbanas. ThinkHazard califica como alta la amenaza por inundación
urbana en Leticia [@thinkhazard2024]. El 22 de septiembre de 2024 un vendaval afectó los 32 barrios y llevó a
declarar la calamidad pública [@elpais2024vendaval].

## Preguntas

1. ¿Qué tan intensa es la lluvia diaria extrema y está cambiando?
2. ¿Con qué frecuencia hay vendavales y qué daños dejan?
3. ¿Dónde se acumula el agua de lluvia en la ciudad?
4. ¿Cómo cambiará la lluvia extrema?

## Cadena de análisis

```{mermaid}
flowchart LR
  ERA[ERA5 lluvia y rachas] --> RX[Rx1day, Rx5day, R20mm]
  RX --> GEV[GEV de Rx1day]
  REG[DesInventar y UNGRD] --> V[Registro de vendavales]
  DEM[Copernicus DEM] --> DEP[Depresiones topográficas]
  E[Edificaciones] --> X[Exposición a encharcamiento]
  DEP --> X
  CCKP[CMIP6 CCKP] --> ESC[Rx1day, Rx5day, R20mm futuros]
```

## Datos y métodos

ERA5 [@hersbach2020]; GEV por L-momentos [@hosking1985]; DesInventar [@desinventar] y UNGRD
[@ungrd2026emergencias]; Copernicus DEM [@copernicusdem2021]; proyecciones del CCKP [@cckp2024].

## Limitaciones

- ERA5 no resuelve tormentas convectivas: subestima la lluvia puntual y las rachas. Las curvas IDF del IDEAM para el
  aeropuerto Vásquez Cobo deben reemplazar estas cifras para diseño.
- Las depresiones del modelo de superficie incluyen claros entre árboles y patios: es un indicador de tamizaje.
- Sin datos del material de las cubiertas no es posible mapear la vulnerabilidad a vendavales.
