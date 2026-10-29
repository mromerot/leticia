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

(conceptos-medidas)=
## Reducción del riesgo, mitigación y adaptación

Las medidas de las páginas *e* de cada flujo de la sección 3 usan tres conceptos que se cruzan y que conviene
distinguir. El más delicado es **mitigación**, que significa cosas distintas en la gestión del riesgo de desastres
y en la política de cambio climático.

```{list-table} Tres conceptos en la norma colombiana (texto literal) y cómo se usan en este libro
:header-rows: 1
:label: tabla-conceptos-medidas
* - Concepto
  - Definición normativa
  - Uso en este libro
* - **Reducción del riesgo**
  - «Es el proceso de la gestión del riesgo, está compuesto por la intervención dirigida a modificar o disminuir las
    condiciones de riesgo existentes, entiéndase: mitigación del riesgo y a evitar nuevo riesgo en el territorio,
    entiéndase: prevención del riesgo. […] La reducción del riesgo la componen la intervención correctiva del riesgo
    existente, la intervención prospectiva de nuevo riesgo y la protección financiera» (Ley 1523, art. 4, num. 21,
    modificado por la Ley 2474 de 2025) [@ley1523; @ley2474].
  - Es el proceso que agrupa las medidas de **prevención**, **mitigación del riesgo** y **protección financiera**.
* - **Mitigación del riesgo**
  - «Medidas de intervención prescriptiva o correctiva dirigidas a reducir o disminuir los daños y pérdidas que se
    puedan presentar a través de reglamentos de seguridad y proyectos de inversión pública o privada cuyo objetivo es
    reducir las condiciones de amenaza, cuando sea posible, y la vulnerabilidad existente» (Ley 1523, art. 4, num. 16).
  - Medidas que reducen el **riesgo que ya existe**: reforzar, elevar o reubicar lo expuesto, o reducir la amenaza.
* - **Prevención del riesgo**
  - «Medidas y acciones de intervención restrictiva o prospectiva dispuestas con anticipación con el fin de evitar que
    se genere riesgo. […] Los instrumentos esenciales de la prevención son aquellos previstos en la planificación, la
    inversión pública y el ordenamiento ambiental territorial» (Ley 1523, art. 4, num. 18).
  - Medidas que **evitan riesgo nuevo**: sobre todo, el ordenamiento del territorio y las normas de construcción.
* - **Protección financiera**
  - «Mecanismos o instrumentos financieros de retención intencional o transferencia del riesgo que se establecen en
    forma ex ante con el fin de acceder de manera ex post a recursos económicos oportunos para la atención de
    emergencias y la recuperación» (Ley 1523, art. 4, num. 19).
  - Fondos, reservas y seguros que pagan la respuesta y la recuperación.
* - **Adaptación**
  - «Comprende el ajuste de los sistemas naturales o humanos a los estímulos climáticos actuales o esperados o a sus
    efectos, con el fin de moderar perjuicios o explotar oportunidades beneficiosas. En el caso de los eventos
    hidrometeorológicos la Adaptación al Cambio Climático corresponde a la gestión del riesgo de desastres en la
    medida en que está encaminada a la reducción de la vulnerabilidad o al mejoramiento de la resiliencia en
    respuesta a los cambios observados o esperados del clima y su variabilidad» (Ley 1523, art. 4, num. 1). La Ley 1931
    la define como «el proceso de ajuste a los efectos presentes y esperados del cambio climático» (art. 3, num. 2)
    [@ley1931].
  - Una medida es de adaptación cuando responde al **clima que cambia**: a las tendencias observadas en las
    secciones *b* y a los escenarios de las secciones *d*.
* - **Mitigación del cambio climático**
  - «Es la gestión que busca reducir los niveles de emisiones de gases de efecto invernadero en la atmósfera a través
    de la limitación o disminución de las fuentes de emisiones de gases de efecto invernadero y el aumento o mejora de
    los sumideros y reservas de gases de efecto invernadero» (Ley 1931, art. 3, num. 11).
  - No reduce el riesgo local de inmediato, pero muchas medidas de Leticia la producen como **cobeneficio**: frenar
    la deforestación reduce a la vez el fuego, el calor y las emisiones.
```

La misma palabra, entonces, nombra dos cosas. En la Ley 1523, **mitigación del riesgo** es reducir las pérdidas
posibles por una amenaza: elevar una vivienda, reubicarla, reforzar una orilla. En la Ley 1931 y en el IPCC,
**mitigación** es reducir las emisiones de gases de efecto invernadero o aumentar sus sumideros; lo que la gestión
del riesgo llama mitigación, el IPCC lo llama casi siempre **adaptación** [@ipcc2022wg2]. La terminología de la
UNDRR hace la misma advertencia [@undrr_terminologia]. En este libro se escribe siempre «mitigación del riesgo» o
«mitigación del cambio climático» para no confundirlas.

Los conceptos también se solapan. Para las amenazas hidrometeorológicas, que son casi todas las de Leticia, la Ley
1523 asimila la adaptación a la gestión del riesgo cuando reduce la vulnerabilidad o mejora la resiliencia: una
misma medida puede ser **prevención o mitigación del riesgo** y, a la vez, **adaptación** si responde al clima que
cambia.

```{mermaid}
flowchart TB
  GR["Gestión del riesgo de desastres<br/>(Ley 1523)"] --> CO["Conocimiento del riesgo"]
  GR --> RE["Reducción del riesgo"]
  GR --> MA["Manejo de desastres<br/>(preparación, alerta, respuesta)"]
  RE --> PR["Prevención<br/>intervención prospectiva:<br/>evitar riesgo nuevo"]
  RE --> MI["Mitigación del riesgo<br/>intervención correctiva:<br/>reducir el riesgo existente"]
  RE --> PF["Protección financiera"]
  AD["Adaptación al cambio climático<br/>(Ley 1931, IPCC)"] -. "coincide si reduce vulnerabilidad<br/>ante eventos hidrometeorológicos" .- PR
  AD -. coincide .- MI
  AD -. "alerta temprana" .- MA
  MCC["Mitigación del cambio climático<br/>(reducir emisiones, aumentar sumideros)"] -. "cobeneficios: bosque,<br/>arbolado urbano" .- PR
```

Las páginas *e* clasifican cada medida así:

- **Tipo según la Ley 1523**: prevención (intervención prospectiva), mitigación del riesgo (intervención
  correctiva) o protección financiera. Se incluyen también medidas de **preparación** (proceso de manejo), como la
  alerta temprana, porque son de las opciones de adaptación más eficaces, y de **conocimiento**, cuando son la
  condición para que las demás funcionen.
- **Componente**: qué reduce la medida, la amenaza, la exposición o la vulnerabilidad.
- **Adaptación**: si responde a un cambio del clima observado o proyectado en el flujo.
- **Mitigación del cambio climático**: si además reduce emisiones o aumenta sumideros.
