---
title: 3.4.a Descripción — Calor extremo
short_title: a. Descripción
---

## La amenaza en Leticia

Leticia tiene un clima ecuatorial cálido y muy húmedo: máximas de 30–32 °C casi todo el año y humedad del 80–90 %.
El calor afecta la salud cuando la temperatura y la humedad impiden que el cuerpo se enfríe, sobre todo de noche. La
Amazonía se calienta de forma clara desde 1980 [@marengo2021spa22] y en 2023 vivió cuatro olas de calor de 2–5 °C
sobre lo normal [@costa2023spa; @espinoza2024]. Dentro de la ciudad, los techos de zinc, el pavimento y la pérdida de
árboles crean islas de calor.

## Preguntas

1. ¿Cuánto se ha calentado Leticia y cuántos días calurosos hay ahora?
2. ¿Dónde hace más calor dentro de la ciudad y quién vive allí?
3. ¿Cuántos días calurosos, noches tropicales y días con índice de calor peligroso habrá con cada escenario?

## Cadena de análisis

```{mermaid}
flowchart LR
  ERA[ERA5 diario 1950–2026] --> TR[Tendencia Tmax]
  ERA --> U[Umbral p90 local] --> O[Días y olas de calor]
  ERA --> TA[Temperatura aparente]
  L[Landsat 8/9 jul–oct] --> LST[Temperatura de superficie y NDVI]
  LST --> B[Mapa bivariado<br/>calor × vulnerabilidad]
  E[Edificaciones y población] --> B
  CCKP[CMIP6 CCKP] --> P[Tmax, hi35, tr26]
  P --> DEL[Método delta:<br/>días sobre el umbral actual]
  U --> DEL
```

## Datos y métodos

ERA5 [@hersbach2020]; temperatura aparente de Steadman [@steadman1984]; temperatura de superficie de Landsat 8/9;
proyecciones del CCKP [@cckp2024; @thrasher2022]; umbrales relativos y olas de al menos tres días, como en CLIMAAX
[@climaax2026handbook].

## Limitaciones

- ERA5 representa una celda de ~28 km dominada por bosque: subestima el calor urbano.
- La temperatura de superficie a media mañana no es la temperatura del aire, pero ordena bien los lugares.
- Sin datos de edad e ingreso por manzana, la vulnerabilidad se aproxima con densidad, población y vegetación.
