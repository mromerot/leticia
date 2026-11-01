---
title: 1.4 Cómo se organiza una evaluación
short_title: 1.4 Proceso de evaluación
---

## Los pasos de CLIMAAX

El manual CLIMAAX organiza la evaluación del riesgo climático en cinco pasos [@climaax2026handbook]:

1. **Definición del alcance** (*scoping*): objetivos, territorio, actores y amenazas candidatas.
2. **Exploración del riesgo**: revisión de evidencia y tamizaje de amenazas con datos disponibles.
3. **Análisis del riesgo**: flujos de trabajo cuantitativos por amenaza (amenaza, exposición, vulnerabilidad).
4. **Evaluación de riesgos clave**: síntesis, comparación y priorización.
5. **Seguimiento y aprendizaje**: monitoreo, actualización y uso en la planificación.

## Cómo se aplica en este libro

```{list-table}
:header-rows: 1
* - Paso CLIMAAX
  - Dónde está en el libro
* - 1. Alcance
  - [1.5 Leticia: el territorio](15_contexto_leticia.md) y [2.6 Área de estudio](../02_datos/26_area_estudio.ipynb)
* - 2. Exploración
  - [1.6 Revisión de la evidencia](16_evidencia.md), [1.7 Perfil de riesgos](17_perfil_riesgos.ipynb), con la
    matriz de priorización, y [1.8 Flujos de la literatura](18_revision_literatura.md)
* - 3. Análisis
  - Siete flujos de la [Sección 3](../03_analisis/index.md), cada uno con las páginas a (descripción), b (amenaza),
    c (riesgo), d (escenarios) y e (medidas de reducción del riesgo y adaptación)
* - 4. Riesgos clave
  - [3.8 Síntesis multiamenaza](../03_analisis/38_sintesis.ipynb)
* - 5. Seguimiento
  - Cuadernos reproducibles en Colab que se pueden volver a ejecutar cada año con datos nuevos
```

## Niveles de respaldo de los datos

Como SIDRo, cada capa del [catálogo](../02_datos/25_catalogo.md) declara su nivel: **local** (Alcaldía,
Corpoamazonia), **nacional** (IDEAM, UNGRD, DANE) o **global** (Copernicus, NASA, Banco Mundial). Para Leticia casi
no hay capas locales abiertas: los estudios de amenaza del PMGRD y del PBOT no están publicados como datos. Por eso
el libro usa la mejor información nacional disponible —la serie de nivel del IDEAM es excepcional por su longitud—
y la complementa con productos globales. Cuando existan capas locales, basta con añadirlas al catálogo.

## Reproducibilidad

- **Todo en cuadernos.** Cada página b, c y d es un cuaderno de Jupyter que descarga los datos de su fuente
  original, los procesa con el paquete `leticia` y genera las cifras del texto.
- **Configuración separada del código.** Lo específico del territorio (extensiones, estación del IDEAM, umbrales,
  pesos) vive en `config/*.yaml`.
- **Ejecución en la nube.** Los cuadernos se ejecutan en Google Colab sin instalar nada; las salidas publicadas en
  este sitio provienen de una ejecución completa en la nube con datos reales (octubre de 2026).
