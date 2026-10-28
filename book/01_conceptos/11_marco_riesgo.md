---
title: 1.1 Amenaza, exposición, vulnerabilidad y riesgo
short_title: 1.1 Marco de riesgo
---

## El marco H × E × V

El riesgo de desastres se expresa como función de tres componentes [@amadio2024ccdr]:

- la **amenaza** (*H*, de *hazard*): la probabilidad de ocurrencia y la intensidad de un fenómeno en un lugar;
- la **exposición** (*E*): las personas, viviendas, infraestructura y medios de vida situados en ese lugar;
- la **vulnerabilidad** (*V*): las condiciones físicas, sociales, económicas y ambientales que aumentan la
  susceptibilidad de lo expuesto a sufrir daño.

El manual CLIMAAX lo resume en **AMENAZA × EXPOSICIÓN × VULNERABILIDAD = RIESGO** y subraya que los tres
componentes cambian en el tiempo [@climaax2026handbook]. El IPCC añade las **respuestas** humanas, que pueden
reducir el riesgo o, mal diseñadas, aumentarlo [@arabegum2022].

```{mermaid}
flowchart LR
  H["Amenaza<br/>crecientes, vaciantes, calor,<br/>fuego, lluvias, vendavales"] --> R(("Riesgo"))
  E["Exposición<br/>personas, edificaciones,<br/>puerto, acueducto, bosque"] --> R
  V["Vulnerabilidad<br/>física · social · sistémica"] --> R
  C["Respuesta / adaptación"] -. modifica .-> E
  C -. modifica .-> V
  C -. puede modificar .-> H
  R --> I["Impacto esperado<br/>daños, personas afectadas,<br/>días de aislamiento"]
```

## Definiciones

```{list-table} Definiciones de referencia (traducciones propias salvo la Ley 1523)
:header-rows: 1
* - Término
  - Internacional
  - Ley 1523 de 2012 (art. 4)
* - **Riesgo**
  - IPCC: el potencial de consecuencias adversas para los sistemas humanos o ecológicos. UNDRR: la probabilidad de
    pérdida de vidas, lesiones o destrucción y daño por un desastre en un periodo dado [@undrr_terminologia].
  - Daños o pérdidas potenciales que pueden presentarse debido a los eventos físicos peligrosos; se deriva de la
    combinación de la amenaza y la vulnerabilidad [@ley1523].
* - **Amenaza**
  - IPCC: la ocurrencia potencial de un evento o tendencia física natural o inducida por el ser humano [@ipcc2022wg2].
  - Peligro latente de que un evento físico de origen natural, o causado o inducido por la acción humana, se presente
    con una severidad suficiente para causar daños [@ley1523].
* - **Exposición**
  - IPCC: la presencia de personas, medios de vida, especies o ecosistemas, funciones, servicios, infraestructura o
    bienes en lugares que podrían verse afectados [@ipcc2022wg2].
  - Presencia de personas, medios de subsistencia, servicios ambientales y otros bienes que por su localización
    pueden ser afectados [@ley1523].
* - **Vulnerabilidad**
  - IPCC: la propensión o predisposición a ser afectado negativamente, que incluye la sensibilidad al daño y la falta
    de capacidad de respuesta y adaptación [@ipcc2022wg2].
  - Susceptibilidad o fragilidad física, económica, social, ambiental o institucional de una comunidad a ser
    afectada por un evento físico peligroso [@ley1523].
```

## Amenaza: intensidad, frecuencia y periodo de retorno

La intensidad de la amenaza puede representarse de forma **determinista** (un escenario, un evento histórico) o
**probabilista**, con capas de intensidad asociadas a una frecuencia expresada como **periodo de retorno** *T*: el
nivel que se iguala o supera en promedio una vez cada *T* años, con probabilidad anual 1/*T* [@amadio2024ccdr].
En Leticia, la amenaza fluvial se describe con la **regla del IDEAM**: un nivel de 18,4 m corresponde hoy a una
creciente de ~100 años, y uno de 4 m a una vaciante de ~10 años ([3.1](../03_analisis/31_inundacion/index.md),
[3.2](../03_analisis/32_sequia/index.md)). Los periodos de retorno se estiman ajustando una distribución
generalizada de valores extremos (GEV) a los máximos o mínimos anuales [@coles2001extremes; @hosking1985].

## Exposición

La exposición son los **receptores del riesgo**. En este libro se representan con las **huellas de edificaciones**
de Microsoft [@microsoft2023buildings], la **población** de Kontur repartida entre esas edificaciones
[@kontur2023] y una **malla de celdas de 200 m** que permite comparar amenazas en el mismo soporte espacial
([2.6](../02_datos/26_area_estudio.ipynb)). En Leticia la exposición es también **sistémica**: toda la ciudad
depende del río para abastecerse, de modo que una vaciante expone a toda la población aunque no moje una casa.

## Vulnerabilidad física y social

La vulnerabilidad física se cuantifica con **funciones de daño** que relacionan la intensidad con la fracción de
valor perdido; para inundación se usa la curva profundidad–daño residencial para Suramérica de Huizinga et al.
[@huizinga2017]. La vulnerabilidad social y la sensibilidad se aproximan con **índices** (densidad construida,
población, cercanía al río, falta de vegetación) cuyos pesos se declaran en `parametros.yaml`.

## Del impacto al riesgo: pérdida anual esperada

Con varios escenarios de periodo de retorno se construye la **curva de excedencia**; el área bajo esa curva es el
**impacto anual esperado**:

$$
EAI \approx \sum_{k} I_k \, \Delta p_k
$$ (eq-eai)

donde $I_k$ es el impacto del escenario $k$ y $\Delta p_k$ el intervalo de probabilidad anual de excedencia que
representa [@amadio2024ccdr]. Cuando no hay función de daño se reporta la **exposición anual esperada**.

## Clases relativas de riesgo

Para comparar amenazas dentro de la ciudad, cada flujo transforma sus indicadores en rangos percentiles (0–1), los
agrupa en cinco clases (muy baja a muy alta) y las cruza en una matriz amenaza × vulnerabilidad. Son clases
**relativas a Leticia**, útiles para priorizar, no categorías absolutas como las de un estudio de amenaza oficial.
