---
title: 3.3.a Descripción — Erosión de orillas y dinámica fluvial
short_title: a. Descripción
---

## La amenaza en Leticia

El Amazonas erosiona sus orillas cóncavas y sedimenta en las convexas; las islas migran río abajo y los brazos
cambian de caudal [@pigcct2022amazonas]. Frente a Leticia, la isla de Santa Rosa surgió hace unos 50 años y,
según estudios de la Universidad Nacional, la fracción del caudal que pasa por el lado colombiano bajó de ~30 % a
~19,5 % entre 1993 y 2025 [@rtvc2025sedimentacion]. La consecuencia es doble: **erosión** donde el río se acerca
(barrancos, muelles, viviendas ribereñas) y **sedimentación** donde se aleja (pérdida de acceso al canal navegable y
de agua para la quebrada Yahuarcaca [@bluradio2022agua]). En 2025 Colombia y Perú acordaron estudios técnicos y un
plan de monitoreo del sector Atacuari–Leticia [@forbes2025navegabilidad].

## Preguntas

1. ¿Cómo cambió el cauce en aguas bajas entre 1987 y 2024?
2. ¿Dónde hubo erosión y dónde sedimentación?
3. ¿Qué edificaciones están en la franja de orilla activa?
4. ¿Cómo cambia el agua disponible frente a la ciudad y qué implica para el puerto?

## Cadena de análisis

```{mermaid}
flowchart LR
  L[Landsat 5–9<br/>ago–nov 1987, 2001, 2013, 2024] --> M[MNDWI > 0<br/>máscaras de agua]
  M --> C[Erosión y sedimentación]
  G[JRC GSW transiciones] --> C
  M --> O[Orilla de aguas bajas] --> F[Franja de 150 m]
  E[Edificaciones] --> X[Exposición]
  F --> X
  M --> A[Agua frente a la ciudad] --> T[Tendencia a nivel constante]
  N[Nivel IDEAM] --> T
```

## Datos y métodos

Compuestos de mediana Landsat Collection 2 con nubes enmascaradas; agua con MNDWI [@xu2006mndwi]; transiciones del
JRC GSW [@pekel2016]; edificaciones de Microsoft [@microsoft2023buildings].

## Limitaciones

- Comparar años de aguas bajas mezcla el cambio de forma del cauce con la diferencia de nivel; se mitiga con las
  transiciones del JRC y con una regresión que descuenta el nivel.
- Landsat (30 m) no ve la socavación de pocos metros que destruye una vivienda: la franja de 150 m es un criterio
  de tamizaje para priorizar estudios geotécnicos y monitoreo con drones o topografía.
