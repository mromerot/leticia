# Leticia — riesgos de desastres y climáticos

[![Libro](https://img.shields.io/badge/libro-mromerot.github.io%2Fleticia-0b5c8e)](https://mromerot.github.io/leticia/)
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mromerot/leticia/blob/main/book/01_conceptos/17_perfil_riesgos.ipynb)
[![Pruebas](https://github.com/mromerot/leticia/actions/workflows/pruebas.yml/badge.svg)](https://github.com/mromerot/leticia/actions/workflows/pruebas.yml)
[![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-blue)](LICENSE)
[![Contenido: CC BY 4.0](https://img.shields.io/badge/contenido-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

Análisis reproducible de los **riesgos de desastres y climáticos de Leticia** (Amazonas, Colombia), organizado con la
estructura de [SIDRo](https://mromerot.github.io/SIDRo/): conceptos y evidencia, fuentes de datos y siete flujos de
análisis (inundación fluvial, sequía y estiaje, erosión y dinámica fluvial, calor extremo, incendios y humo, lluvias
intensas y vendavales, y dengue y clima), cada uno con descripción, amenaza, riesgo, escenarios y medidas de
reducción del riesgo, mitigación y adaptación, más una síntesis multiamenaza. Los métodos de la literatura científica reproducidos para Leticia se resumen en la página 1.8.

Todo el análisis está en **cuadernos de Jupyter compatibles con Google Colab** que descargan los datos de sus fuentes
oficiales (IDEAM, UNGRD, DesInventar, Copernicus, NASA, Banco Mundial, Microsoft Planetary Computer) y usan el
paquete `leticia` de este repositorio. El libro se publica con [MyST](https://mystmd.org) en
**https://mromerot.github.io/leticia/**.

## Resultados clave

- **Sequía y estiaje:** en septiembre de 2024 el río bajó a **2,24 m** en la regla del IDEAM, 2,2 m por debajo del
  mínimo previo (2010); 52 días bajo 4 m.
- **Inundación fluvial:** crecientes de 18,4–18,5 m en 1999, 2012 y 2015; la de 100 años expone ~1 700 edificaciones.
- **Erosión y sedimentación:** ~1 700 ha de bancos e islas nuevos frente a la ciudad entre 1987 y 2024.
- **Calor:** +0,22 °C por década en la máxima desde 1980; hasta 10 °C más en superficie en el centro que en el bosque.
- **Incendios y vendavales:** máximos de focos de calor e incendios registrados en 2024; vendavales casi anuales.
- **Dengue:** 4 366 casos notificados en 2007–2022, con el brote de 2019 (1 716); la temperatura media se acerca al
  óptimo de transmisión de *Aedes aegypti*.
- **Métodos de la literatura:** la vaciante de 2024 tuvo 132 días bajo el P80 (Santos de Lima et al., 2024); la
  orilla del Amazonas cerca de Leticia retrocede 2–15 m/año (REAL); GloFAS adelanta unas cuatro semanas el pico de
  la creciente.

## Ejecutar

En Colab: abra cualquier cuaderno desde el libro con el botón **Open in Colab**. En local:

```bash
git clone https://github.com/mromerot/leticia && cd leticia
pip install -e ".[libro,dev]"
pytest
jupyter lab
myst start
```

## Estructura

```
myst.yml, index.md        configuración y portada del libro
book/01_conceptos/        conceptos, contexto, revisión de evidencia, perfil de riesgos (cuaderno) y flujos de la literatura
book/02_datos/            fuentes de datos, catálogo y área de estudio (cuaderno)
book/03_analisis/         siete flujos (a. descripción, b. amenaza, c. riesgo, d. escenarios, e. medidas) y síntesis
book/recursos/            Colab, glosario, software, preguntas frecuentes y cómo citar
src/leticia/              paquete de Python (fuentes, hidro, clima, espacial, exposicion, riesgo, pronostico, salud, viz)
src/leticia/config/       aoi.yaml, sources.yaml, parametros.yaml: todo lo específico del territorio
tests/                    pruebas con datos sintéticos
```

## Publicación

Los cuadernos se ejecutan en la nube con datos reales y sus salidas se guardan en los `.ipynb`. El flujo
`.github/workflows/publicar.yml` construye el sitio con MyST a partir de esas salidas y lo publica en GitHub Pages.

## Licencias y cita

Contenido CC BY 4.0, código MIT. Ver `CITATION.cff`.
