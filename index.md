---
title: Leticia — riesgos de desastres y climáticos
subtitle: Análisis reproducible para la ciudad de Leticia, Amazonas (Colombia), con la estructura de SIDRo
---

Este libro reúne **datos abiertos, métodos y resultados** para entender los riesgos de desastres y los riesgos
climáticos de **Leticia**, capital del departamento de Amazonas, en la triple frontera con Brasil y Perú. Sigue la
estructura de [SIDRo](https://mromerot.github.io/SIDRo/) [@romero2026sidro] —conceptos, fuentes de datos y
flujos de análisis por amenaza con cuatro páginas cada uno— y la adapta a una ciudad ribereña amazónica. Todo el
análisis está en **cuadernos de Jupyter que se ejecutan en Google Colab** con un clic, de modo que cada cifra y
cada mapa se pueden reproducir desde su fuente.

:::{important} Resultados clave
- **Sequía y estiaje.** En septiembre de 2024 el Amazonas bajó a **2,24 m** en la regla del IDEAM en Leticia,
  2,2 m por debajo del mínimo anterior del registro (2010). El río pasó 52 días por debajo de 4 m, cuando antes de
  2023 nunca lo había estado. Con la estadística de 1988–2022, una vaciante así era imposible; hoy tiene un
  periodo de retorno de pocas décadas.
- **Inundación fluvial.** Las grandes crecientes (18,4–18,5 m en 1999, 2012 y 2015) son la amenaza con más
  personas afectadas en la historia de la ciudad. El mapa de 100 años del JRC expone unas **1 700 edificaciones** y
  cada metro adicional de creciente aumenta en más de 50 % la población expuesta.
- **Erosión y dinámica fluvial.** Entre 1987 y 2024 el tramo del río frente a Leticia ganó ~1 700 ha de bancos e
  islas y perdió ~900 ha de agua en aguas bajas: la sedimentación aleja el canal navegable de la ciudad.
- **Calor extremo.** La temperatura máxima sube **0,2 °C por década** desde 1980. El centro construido es hasta
  10 °C más caliente en superficie que el bosque vecino. Con SSP2-4.5, los días con índice de calor sobre 35 °C
  pasarían de ~7 a ~90 por año hacia 2050.
- **Incendios, lluvias intensas y vendavales** completan el perfil: 2024 tuvo el máximo de focos de calor y de
  incendios de cobertura vegetal registrados, y desde 2021 hay vendavales casi todos los años.
:::

## ¿A quién sirve?

- A la **Alcaldía de Leticia**, el **Consejo Municipal de Gestión del Riesgo** y la **Gobernación de Amazonas**,
  como punto de partida cuantitativo para actualizar el PMGRD (2013) e integrar el PIGCCT de Amazonas (2022).
- A **Corpoamazonia, el IDEAM, la Capitanía de Puerto y la UNGRD**, como plantilla abierta para el monitoreo del río,
  el cauce y el clima.
- A **investigadores y comunidades**, para ver cómo se construye un diagnóstico y qué datos lo sustentan.

:::{warning} Alcance
Los resultados son **indicativos**: combinan datos globales y nacionales de 10 a 90 m de resolución y supuestos
documentados en `parametros.yaml`. No reemplazan los estudios básicos y detallados de amenaza que exige la norma
colombiana ni los conceptos técnicos del IDEAM y la UNGRD.
:::

## Cómo está organizado

| Sección | Contenido |
|---|---|
| [1. Conceptos y evidencia](book/01_conceptos/index.md) | Marco de riesgo, riesgo climático, marco normativo, proceso de evaluación, contexto de Leticia, **revisión de la evidencia** (OTCA, Panel Científico por la Amazonía, IDEAM, UNGRD), **perfil de riesgos** con datos y **flujos de trabajo de la literatura científica** |
| [2. Fuentes de datos](book/02_datos/index.md) | Amenaza, exposición, clima, otros datos, catálogo y cuaderno del área de estudio |
| [3. Análisis](book/03_analisis/index.md) | Siete flujos de trabajo (inundación, sequía, erosión, calor, incendios, lluvias y vendavales, y dengue), cada uno con descripción, amenaza, riesgo y escenarios, y una síntesis multiamenaza |
| [Recursos](book/recursos/colab.md) | Cómo ejecutar en Colab, glosario, software, preguntas frecuentes y cómo citar |

## Cómo usarlo

Cada cuaderno tiene un botón **«Open in Colab»**. Colab instala el paquete del proyecto desde GitHub y descarga los
datos de las fuentes oficiales al ejecutarse. Para trabajar en local:

```bash
git clone https://github.com/mromerot/leticia && cd leticia
pip install -e ".[libro]"
jupyter lab                       # abra cualquier cuaderno de book/
myst start                        # vista previa del libro
```

## Créditos

Estructura y métodos de **SIDRo** [@romero2026sidro], **CCDR-tools** (GFDRR, Banco Mundial) [@amadio2024ccdr] y el
**CLIMAAX Climate Risk Assessment Handbook** [@climaax2026handbook]. Evidencia de la OTCA [@otca2021atlas], el Panel
Científico por la Amazonía [@marengo2021spa22; @marengo2024spa], el IDEAM [@ideam2017tcncc; @ideam2024comunicado100]
y la UNGRD. Autor: Mauricio Romero. Contenido bajo CC BY 4.0; código bajo MIT.
