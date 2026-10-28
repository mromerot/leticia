---
title: 3.1.a Descripción — Inundación fluvial
short_title: a. Descripción
---

## La amenaza en Leticia

El Amazonas frente a Leticia es un río de llanura con un **pulso de inundación** anual: sube desde octubre, alcanza
su máximo entre abril y junio y baja hasta septiembre [@junk1989]. Las comunidades ribereñas, la várzea y los lagos
de Yahuarcaca dependen de ese pulso. La amenaza aparece cuando la creciente es más alta o más larga de lo habitual,
como en 1999, 2012 y 2015. El agua entra a los barrios ribereños y de quebradas, a las viviendas palafíticas y a las
chagras; interrumpe servicios y obliga a evacuar.

La evidencia regional muestra que las grandes crecientes amazónicas se han vuelto más frecuentes desde el año 2000
[@marengo2021spa22; @barichivich2018], y DesInventar registra 49 inundaciones con más de cien mil afectados
acumulados en Amazonas en 1990–2015 [@pigcct2022amazonas].

## Preguntas

1. ¿Cuál es el nivel de la creciente de 2, 10, 50 y 100 años en la regla de Leticia?
2. ¿Hay tendencia en las crecientes de las últimas décadas?
3. ¿Cuántas edificaciones y personas quedan expuestas en cada periodo de retorno y cuál es la pérdida anual esperada?
4. ¿Cuánto aumentaría la exposición si las crecientes subieran 0,5 o 1 m más?

## Cadena de análisis

```{mermaid}
flowchart LR
  N[Nivel diario IDEAM<br/>1987–2026] --> QC[Control de calidad]
  QC --> MX[Máximos anuales]
  MX --> GEV[GEV por L-momentos<br/>periodos de retorno]
  MX --> MK[Tendencia<br/>Mann-Kendall]
  Q[Caudal GloFAS] --> RNC[Relación nivel–caudal]
  RNC --> PRON[Pronóstico en la regla]
  JRC[Mapas JRC<br/>RP10–RP500] --> EXP[Edificaciones y<br/>personas expuestas]
  E[Edificaciones y población] --> EXP
  EXP --> DAN[Curva de daño<br/>Huizinga] --> PAE[Pérdida anual esperada]
  DEM[Copernicus DEM] --> HAND[Altura sobre el río] --> SENS[Sensibilidad +0,5 / +1 m]
```

## Datos y métodos

- **Amenaza:** serie IDEAM [48017010] [@ideam2026niveles]; GloFAS v4 [@grimaldi2022glofas]; mapas del JRC
  [@baugh2024jrc]; ocurrencia de agua JRC GSW [@pekel2016].
- **Exposición:** edificaciones de Microsoft y población de Kontur ([2.6](../../02_datos/26_area_estudio.ipynb)).
- **Vulnerabilidad:** curva profundidad–daño residencial de Suramérica [@huizinga2017]; índice de vulnerabilidad de la
  malla (densidad, población, cercanía al río, vegetación).
- **Escenarios:** lluvia media y extrema del CCKP [@cckp2024]; sensibilidad con la altura sobre el río
  [@renno2008hand].

## Limitaciones

- Los mapas del JRC (90 m) no conocen el malecón, los rellenos ni las viviendas palafíticas; sobrestiman la
  profundidad en algunas celdas y la subestiman en otras.
- El modelo de superficie incluye árboles y techos: la altura sobre el río es un indicador relativo.
- Con 38 años de datos, los niveles de 50 y 100 años son extrapolaciones con incertidumbre.
- **Recomendación:** un modelo hidráulico local con batimetría y topografía LiDAR de la franja ribereña.
