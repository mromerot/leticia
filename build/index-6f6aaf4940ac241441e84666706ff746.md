---
title: EVA — Evaluación y análisis de riesgos de desastres
short_title: Inicio
subtitle: Riesgos de desastres y climáticos de Leticia, Amazonas (Colombia), con datos abiertos y cuadernos reproducibles
---

**EVA** reúne datos abiertos, métodos y cuadernos reproducibles para evaluar y analizar los riesgos de desastres y
climáticos de un territorio, amenaza por amenaza y en conjunto. Su primera aplicación es la ciudad de **Leticia**,
en la Amazonía colombiana.

## Resumen

**Problema.** Leticia, capital del departamento de Amazonas, en la triple frontera con Brasil y Perú, depende del río
Amazonas para el transporte, el agua y los alimentos. El río sube y baja unos 10 m cada año, y ese ciclo se ha
vuelto más extremo en las dos direcciones: grandes crecientes en 1999, 2012 y 2015, y la vaciante récord de 2024. A
eso se suman la erosión y la sedimentación del cauce, el calor, los incendios y el humo, las lluvias intensas, los
vendavales y el dengue. El Plan Municipal de Gestión del Riesgo de Desastres es de 2013, la literatura científica
sobre los riesgos de la ciudad es escasa y no existía una evaluación cuantitativa, abierta y reproducible.

**Objetivo.** Estimar la amenaza, la exposición y el riesgo de siete riesgos de la ciudad (inundación fluvial,
sequía y estiaje, erosión y dinámica fluvial, calor extremo, incendios y humo, lluvias intensas y vendavales, y
dengue) en el clima actual y con escenarios de cambio climático, y derivar de los resultados medidas de reducción del
riesgo y de adaptación.

**Métodos.** Se integraron 33 fuentes de datos abiertos, nacionales y globales. Entre ellas están la serie diaria del
nivel del río del IDEAM en Leticia (38 años con datos suficientes), el pronóstico GloFAS y los mapas de inundación
del JRC. También se usaron imágenes Landsat y Sentinel-2, el agua superficial del JRC y las tasas de erosión de
orillas de REAL. El clima viene del reanálisis ERA5 y del ensamble CMIP6. Se añadieron los focos de calor de FIRMS,
las coberturas y puntos de calor del Instituto SINCHI y la pérdida de bosque de Hansen. La exposición combina
huellas de edificaciones, población de Kontur, registros de desastres de la UNGRD y DesInventar, y casos de dengue
de OpenDengue.

Los métodos son los siguientes:

- Extremos ajustados con la distribución GEV por L-momentos.
- Sequía medida con el SPEI y con la duración de las aguas bajas.
- Pérdida anual esperada calculada con CLIMADA y estrés térmico con el UTCI.
- Pronósticos de la temporada de incendios y del dengue evaluados frente a la climatología con validación cruzada.
- Exposición en una malla de celdas de 200 m, con la población repartida entre las edificaciones.

El análisis de EVA está en un paquete de Python y en cuadernos que se ejecutan en Google Colab.

**Resultados.**

- **Sequía y estiaje.**
  - El 26 de septiembre de 2024 el río bajó a **2,24 m**, 2,2 m por debajo del mínimo anterior (2010), y pasó
    52 días por debajo de 4 m.
  - Con la estadística de 1988–2022 ese nivel era imposible; hoy bajar de 4 m tiene una probabilidad anual cercana
    al 9 %.
  - En la vaciante, la población ribereña a menos de 1 km del cauce navegable bajó de 85 % a 63 %.
- **Inundación fluvial.**
  - La creciente de 100 años (18,4 m) alcanza unas **1 740 edificaciones** y 5 500 personas.
  - La pérdida anual esperada está entre 25 600 y 37 700 millones de pesos, con un costo de reposición
    ilustrativo.
  - Si las crecientes suben 0,5–1 m, la población expuesta crece 22–56 %.
- **Erosión y dinámica fluvial.**
  - La orilla del cauce principal retrocede **2–15 m por año**, hasta diez veces la mediana mundial.
  - El brazo colombiano frente a la ciudad se sedimenta.
  - 83 edificaciones están a menos de 150 m de la orilla activa.
- **Calor extremo.**
  - La temperatura máxima sube **0,22 °C por década**, y los días calurosos pasaron de ~7 a más de 40 por año.
  - El 14 % de las horas tiene estrés por calor fuerte, incluso a la sombra.
  - Con el escenario SSP2-4.5, hacia 2050 habría ~92 días al año con índice de calor sobre 35 °C.
- **Incendios, lluvias y dengue.**
  - **Incendios.** Hay pocos focos de fuego cerca de la ciudad, con el máximo en 2024, pero 308 edificaciones están
    en la interfaz con la vegetación y cerca de focos recientes.
  - **Vendavales.** Desde 2021 hay vendavales casi todos los años.
  - **Dengue.** En más de la mitad de los meses, la temperatura media ya está en el rango de máxima transmisión.
- **Varias amenazas a la vez.** Unas 1 400 edificaciones (~7 800 personas) tienen dos o más amenazas en su quintil
  más alto, sobre todo en la franja ribereña.

**Conclusiones.** El riesgo de Leticia está dominado por un río cuyo ciclo se vuelve más extremo en las dos
direcciones.

- **Sequía.** Es el riesgo nuevo y el de mayor alcance: afecta a toda la ciudad a través del transporte, el agua y
  los precios. Además se encadena con incendios, humo y calor, como ocurrió en 2023–2024.
- **Inundación y erosión.** Se concentran en la franja ribereña y en las zonas bajas.
- **Calor.** Pesa más en el centro denso.
- **Fuego.** Se concentra en la periferia.

Los datos abiertos permiten un primer diagnóstico cuantitativo. Sin embargo, con resoluciones de 10 a 90 m los
resultados son indicativos y no reemplazan los estudios de detalle que exige la norma colombiana.

**Implicaciones.** Los resultados son una base cuantitativa para actualizar el PMGRD y el plan de ordenamiento
territorial (PBOT), y orientan estas medidas:

- Delimitar la franja inundable y el retiro de la orilla activa.
- Fijar umbrales de alerta en la regla de Leticia.
- Asegurar fuentes alternas de agua y el acceso al río en las vaciantes.
- Reducir el calor con vegetación y sombra.
- Manejar el fuego con las autoridades indígenas.
- Dimensionar la protección financiera con la pérdida anual esperada.

Las brechas prioritarias son tres: un modelo hidráulico local con batimetría y topografía LiDAR, datos de
vulnerabilidad por manzana y la continuidad de la serie del IDEAM en aguas bajas. Como todo el flujo está
parametrizado, puede replicarse en otras ciudades ribereñas de la Amazonía cambiando la configuración.

**Palabras clave:** riesgo de desastres · riesgo climático · Amazonía · Leticia · sequía · inundación fluvial ·
datos abiertos · ciencia reproducible

:::{figure} #fig-mapa-area
:label: fig-area-estudio
:class: col-page-right
**Área de estudio.**

- **(a)** Localización de Leticia en el norte de Suramérica.
- **(b)** Municipio de Leticia (DANE) en la triple frontera con Brasil y Perú. En azul, el agua superficial del JRC
  (ocurrencia ≥ 50 % en 1984–2021); en rojo, el área urbana de análisis.
- **(c)** Ciudad y río Amazonas sobre un mosaico Sentinel-2 de 2023–2025. Se marcan el área urbana de análisis, el
  límite municipal y la estación hidrológica del IDEAM.

Fuentes: Natural Earth, DANE (vía geoBoundaries), JRC Global Surface Water y ESA Copernicus. Detalle en el
[cuaderno 2.6](book/02_datos/26_area_estudio.ipynb).
:::

## Cómo está organizado

| Sección | Contenido |
|---|---|
| [1. Conceptos y evidencia](book/01_conceptos/index.md) | **Marco y contexto.** Marco de riesgo, riesgo climático, marco normativo, proceso de evaluación y contexto de Leticia. **Evidencia.** Revisión de la OTCA, el Panel Científico por la Amazonía, el IDEAM y la UNGRD; perfil de riesgos con datos; flujos de trabajo de la literatura científica |
| [2. Fuentes de datos](book/02_datos/index.md) | Amenaza, exposición, clima, otros datos, catálogo y cuaderno del área de estudio |
| [3. Análisis](book/03_analisis/index.md) | **Flujos.** Siete flujos de trabajo con descripción, amenaza, riesgo, escenarios y medidas de reducción del riesgo y adaptación. **Síntesis.** Una síntesis de todas las amenazas |
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

La estructura y los métodos siguen **CCDR-tools** (GFDRR, Banco Mundial) [@amadio2024ccdr] y el **CLIMAAX Climate
Risk Assessment Handbook** [@climaax2026handbook]. La evidencia proviene de la OTCA [@otca2021atlas], del Panel
Científico por la Amazonía [@marengo2021spa22; @marengo2024spa], del IDEAM [@ideam2017tcncc;
@ideam2024comunicado100] y de la UNGRD. Autor: Mauricio Romero. Contenido bajo CC BY 4.0; código bajo MIT.
