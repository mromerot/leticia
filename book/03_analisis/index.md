---
title: 3. Análisis
short_title: 3. Análisis
---

Seis flujos de trabajo, uno por amenaza priorizada en el [perfil de riesgos](../01_conceptos/17_perfil_riesgos.ipynb),
y una síntesis. Como en SIDRo, cada flujo tiene cuatro páginas:

- **a. Descripción**: la amenaza en Leticia, preguntas, cadena de análisis, datos y limitaciones;
- **b. Amenaza** (cuaderno): intensidad, frecuencia y tendencias;
- **c. Riesgo** (cuaderno): cruce con edificaciones, población y vulnerabilidad;
- **d. Escenarios** (cuaderno): cambio climático y sensibilidad.

```{list-table}
:header-rows: 1
* - Flujo
  - Pregunta central
  - Datos principales
* - [3.1 Inundación fluvial](31_inundacion/index.md)
  - ¿Con qué frecuencia y hasta dónde llegan las crecientes del Amazonas?
  - IDEAM (regla de Leticia), GloFAS, JRC, Copernicus DEM
* - [3.2 Sequía y estiaje](32_sequia/index.md)
  - ¿Qué tan probable es otra vaciante como la de 2024 y qué sistemas falla?
  - IDEAM, ERA5 (SPI/SPEI), ONI, Landsat, CCKP
* - [3.3 Erosión y dinámica fluvial](33_erosion/index.md)
  - ¿Cómo ha cambiado el cauce frente a Leticia y qué expone?
  - Landsat 1987–2024, JRC GSW
* - [3.4 Calor extremo](34_calor/index.md)
  - ¿Cuánto se ha calentado Leticia y dónde hace más calor?
  - ERA5, Landsat (temperatura de superficie), CCKP
* - [3.5 Incendios y humo](35_incendios/index.md)
  - ¿Dónde y cuándo hay fuego, y quién está expuesto?
  - NASA FIRMS, Hansen GFC, ESA WorldCover, CCKP
* - [3.6 Lluvias intensas y vendavales](36_lluvias_vendavales/index.md)
  - ¿Qué tan intensos son los aguaceros y dónde se encharca la ciudad?
  - ERA5, DesInventar, UNGRD, Copernicus DEM, CCKP
* - [3.7 Síntesis](37_sintesis.ipynb)
  - ¿Dónde se superponen las amenazas y qué hacer primero?
  - Todos los anteriores
```

:::{tip} Ejecutar en Colab
Cada cuaderno tiene un botón **Open in Colab**. El primer bloque instala el paquete `leticia` desde GitHub; luego
cada cuaderno descarga solo los datos que necesita. Los cuadernos *c* y la síntesis reutilizan la malla de
[2.6](../02_datos/26_area_estudio.ipynb), que se crea sola si no existe.
:::
