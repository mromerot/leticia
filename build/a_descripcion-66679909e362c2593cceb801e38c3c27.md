---
title: 3.7.a Descripción — Dengue y clima
short_title: a. Descripción
---

## La amenaza en Leticia

El dengue es una enfermedad viral transmitida por el mosquito *Aedes aegypti*, que se cría en recipientes con agua
limpia: tanques, canecas, llantas y canaletas. En Leticia también se ha documentado *Aedes albopictus* y sus
criaderos [@carvajal2009aedes]. El clima influye en cada paso de la transmisión: la temperatura acelera el
desarrollo del mosquito y la replicación del virus hasta un óptimo cercano a 29 °C [@mordecai2017], la lluvia y el
almacenamiento de agua multiplican los criaderos, y la humedad prolonga la vida del vector. Leticia es una de las
cuatro ciudades de Colombia para las que Beal et al. evaluaron pronósticos del dengue con información
hidroclimática [@beal2025dengue].

Es un riesgo climático para la salud: el IPCC señala el aumento de las enfermedades transmitidas por vectores entre
los impactos del cambio climático en Centro y Suramérica [@castellanos2022ipcc]. Este flujo se agrega al libro
porque la revisión de literatura ([1.8](../../01_conceptos/18_revision_literatura.md)) encontró un método de
pronóstico aplicado a Leticia.

## Preguntas

1. ¿Cuántos casos se notifican, en qué meses y en qué años hubo brotes?
2. ¿Qué tan favorable es la temperatura de Leticia para la transmisión y cómo ha cambiado?
3. ¿Mejora la información climática un pronóstico del dengue a 1, 3 y 6 meses?
4. ¿Cómo cambia la aptitud térmica con los escenarios de cambio climático?

## Cadena de análisis

```{mermaid}
flowchart LR
  OD[OpenDengue: SIVIGILA semanal 2007–2022] --> M[Casos mensuales]
  ERA[ERA5 diario] --> AN[Anomalías de temperatura,<br/>lluvia y humedad]
  ONI[ONI y TNA] --> AN
  M --> R[Correlaciones con rezago]
  AN --> R
  M --> CE[Canal endémico y brotes]
  M --> P[Pronóstico a 1, 3 y 6 meses<br/>validación dejando un año fuera]
  AN --> P
  ERA --> T[Ventana térmica<br/>Mordecai et al.]
  CCKP[CMIP6 CCKP: temperatura media] --> T
```

## Datos y métodos

Casos semanales notificados al SIVIGILA, compilados por OpenDengue [@clarke2024opendengue]; ERA5 [@hersbach2020];
ONI y TNA de la NOAA [@noaa2026tna]; proyecciones del CCKP [@cckp2024]. Respuesta térmica de la transmisión según
Mordecai et al. [@mordecai2017]. Los modelos de pronóstico replican la comparación de Beal et al. entre modelos
autorregresivos e hidroclimáticos [@beal2025dengue] con regresiones lineales sobre log(1 + casos), un término por
mes calendario y validación cruzada dejando fuera un año completo.

## Limitaciones

- Los casos notificados subestiman la transmisión y dependen del esfuerzo de vigilancia; la serie de 2007–2010 parece
  incompleta y la de OpenDengue termina en 2022.
- Leticia comparte la transmisión con Tabatinga (Brasil) y Santa Rosa (Perú), cuyos casos no se incluyen.
- La temperatura de ERA5 representa una celda de ~28 km dominada por bosque; la ciudad es más caliente.
- La respuesta térmica proviene de experimentos a temperatura constante; la inmunidad de la población, los serotipos
  y el control vectorial no se modelan.
