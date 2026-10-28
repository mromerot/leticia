---
title: 1.8 Flujos de trabajo de la literatura científica
short_title: 1.8 Flujos de la literatura
subtitle: Qué métodos publicados se pueden reproducir para Leticia y cómo se integraron en este libro
---

La sección 1.6 reúne la evidencia sobre **qué** riesgos tiene Leticia. Esta página responde otra pregunta: **¿qué
métodos publicados en la literatura científica se pueden reproducir con datos abiertos para analizar esos riesgos?**
La revisión se hizo en octubre de 2026 y cada flujo encontrado se integró en el cuaderno correspondiente, con sus
resultados para Leticia.

## Cómo se hizo la búsqueda

- **Bases consultadas.** OpenAlex, mediante su API pública [@openalex2026]; Crossref, para verificar autores,
  revistas y DOI; y Zenodo, para los conjuntos de datos y el software. Scopus exige una clave institucional y
  Dimensions una suscripción, así que no se consultaron. Ninguna de las tres tenía un conector disponible en el
  entorno de trabajo.
- **Búsquedas.** Leticia con amenazas (inundación, sequía, erosión, calor, incendios, dengue); migración de cauces y
  erosión de orillas en el Amazonas (incluidas las *terras caídas*); pronóstico y validación de crecientes en la
  cuenca; sequía y navegabilidad; isla de calor y estrés térmico en ciudades amazónicas; pronóstico estacional de
  incendios con la temperatura del mar; dengue y clima en Colombia; y aplicaciones de CLIMADA en Suramérica.
- **Criterios.** Se priorizaron los trabajos que (1) proponen un método reproducible, (2) usan datos abiertos con
  cobertura en Leticia y (3) responden una pregunta de los flujos 3.1–3.6. Cada DOI se verificó en Crossref antes de
  citarlo.

La literatura **sobre Leticia** es escasa en amenazas: la mayoría de los resultados son de biología, salud o
gobernanza. Sobre riesgos aparecieron un estudio de dinámica fluvial entre Nazareth y Leticia [@villadiego2023],
una evaluación de pronósticos de dengue que incluye a Leticia [@beal2025dengue] y un trabajo de 2016 sobre las
causas de las inundaciones en una intersección del centro de la ciudad, sin DOI. La evidencia más útil es regional: la Amazonía brasileña, el Solimões y
la cuenca en conjunto.

## Flujos integrados

```{list-table} Métodos de la literatura reproducidos para Leticia
:header-rows: 1
* - Flujo
  - Método y fuente
  - Resultado para Leticia
  - Dónde está
* - 3.1 Inundación
  - Evaluación de modelos hidrológicos globales frente a estaciones de la cuenca [@towner2019], adaptada a una
    estación que mide nivel y no caudal
  - GloFAS reproduce bien el ciclo anual (correlación diaria 0,87) pero adelanta el pico unas cuatro semanas y
    ordena mal la magnitud de las crecientes de cada año (correlación de los máximos anuales 0,49); las aguas bajas
    las reproduce mejor (0,75)
  - [3.1.b, sección 6](../03_analisis/31_inundacion/b_amenaza.ipynb)
* - 3.2 Sequía
  - Duración de las aguas bajas: días por año hidrológico bajo el P80 de la curva de duración
    [@santosdelima2024]; impactos de la sequía de 2023 [@fleischmann2025]
  - 2024 tuvo el periodo de aguas bajas más largo de los años con registro completo: 132 días bajo el P80
    (9,53 m), del orden de las peores sequías documentadas en Brasil; solo 8 años tienen la temporada completa
  - [3.2.b, sección 4](../03_analisis/32_sequia/b_amenaza.ipynb) y [3.2.c](../03_analisis/32_sequia/c_riesgo.ipynb)
* - 3.2 Sequía
  - Paquete `SPEI` de Python como referencia para el SPI [@vonk2026spei]
  - El SPI-3 del libro coincide con el del paquete (correlación 0,97)
  - [3.2.b, sección 5](../03_analisis/32_sequia/b_amenaza.ipynb)
* - 3.3 Erosión
  - Tasas globales de erosión y acreción de orillas con Landsat, conjunto REAL [@langhorst2023real;
    @langhorst2022realdata]; dinámica Nazareth–Leticia [@villadiego2023]; *terras caídas* [@bandeira2018]
  - En el cauce principal cerca de Leticia la orilla retrocede 2–15 m/año, hasta diez veces la mediana mundial;
    junto a la ciudad la acreción supera a la erosión, como en la sedimentación del brazo colombiano
  - [3.3.b, sección 4](../03_analisis/33_erosion/b_amenaza.ipynb)
* - 3.4 Calor
  - Estrés térmico con el UTCI [@brode2012utci] y su climatología en Suramérica [@miranda2023utci], con la
    implementación del ECMWF [@brimicombe2022thermofeel]; isla de calor de Manaos [@desouza2014manaus]
  - A la sombra, el 14 % de las horas de 1979–2020 tuvo estrés por calor fuerte (UTCI ≥ 32 °C); esas horas
    aumentan unas 14 por año (p = 0,001), con máximos en los años de sequía (2005, 2010, 2015–2016 y 2024)
  - [3.4.b, sección 4](../03_analisis/34_calor/b_amenaza.ipynb)
* - 3.5 Incendios
  - Pronóstico estacional de la temporada de fuego con la temperatura del mar [@chen2011fire] y el índice del
    Atlántico Norte tropical [@fernandes2011]; subestimación de los fuegos pequeños [@randerson2012]
  - En la triple frontera, el TNA de marzo–mayo anticipa con habilidad modesta (0,12) los focos de
    agosto–octubre; los años con más focos (2005, 2010, 2024) tuvieron un Atlántico cálido
  - [3.5.d, sección 2](../03_analisis/35_incendios/d_escenarios.ipynb)
* - 3.7 Dengue (nuevo)
  - Pronóstico del dengue a 1, 3 y 6 meses con información hidroclimática para cuatro ciudades de Colombia,
    entre ellas Leticia [@beal2025dengue]; casos de OpenDengue [@clarke2024opendengue]; respuesta térmica de la
    transmisión [@mordecai2017]
  - Con los datos públicos de 2011–2022 no se reproduce la habilidad hidroclimática a 3–6 meses; el modelo
    autorregresivo es útil a 1 y 3 meses. La temperatura de Leticia se acerca al óptimo de transmisión (29 °C)
  - [3.7 Dengue y clima](../03_analisis/37_dengue/index.md)
```

## Flujos no integrados

- **CLIMADA** [@aznar2019climada] permitiría calcular la pérdida anual esperada por inundación con el mapa del JRC,
  las edificaciones y curvas de daño, con incertidumbre y medidas de adaptación. El libro ya calcula una pérdida
  esperada simple en [3.1.c](../03_analisis/31_inundacion/c_riesgo.ipynb); CLIMADA es una extensión natural, pero
  su instalación en Colab es pesada y se deja como trabajo futuro.
- **Aislamiento de asentamientos.** Santos de Lima et al. también miden la distancia de cada asentamiento al río en
  aguas altas y bajas [@santosdelima2024]. Para Leticia faltaría una capa pública de comunidades ribereñas e
  indígenas del Trapecio Amazónico con su ubicación.
- **Pronóstico de TSM.** Fernandes et al. usaron pronósticos de TSM de un modelo acoplado para anticipar la
  temporada desde abril [@fernandes2011]; aquí se usa la TSM observada de marzo–mayo, que llega en junio.

## Cómo repetir la búsqueda

OpenAlex no exige registro. Por ejemplo, esta consulta devuelve en JSON los trabajos que mencionan a Leticia y la
erosión de orillas:

```text
https://api.openalex.org/works?search=Leticia%20Amazon%20riverbank%20erosion&per-page=25
```

Para ampliar la revisión a Scopus o Dimensions se necesita una clave institucional; con un conector de literatura
científica (por ejemplo, Consensus o PubMed) en el entorno de trabajo, las mismas búsquedas pueden hacerse desde
la sesión de análisis.
