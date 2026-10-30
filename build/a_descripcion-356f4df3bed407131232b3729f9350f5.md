---
title: 3.2.a Descripción — Sequía y estiaje
short_title: a. Descripción
---

## La amenaza en Leticia

La vaciante del Amazonas ocurre cada año entre agosto y noviembre. Cuando es extrema, como en 2010, 2023 y 2024,
los barcos de carga no llegan al puerto, se encarecen los alimentos y el combustible, las comunidades ribereñas
quedan aisladas, se secan lagos y quebradas y muere la fauna acuática [@costa2023spa]. En septiembre de 2024 el IDEAM
reportó niveles por debajo de los mínimos históricos en Leticia [@ideam2024comunicado100]. El Panel Científico por
la Amazonía advierte que las sequías fuertes pasaron de cuatro por siglo a cuatro en menos de 25 años
[@marengo2024spa], y World Weather Attribution atribuyó la de 2023 principalmente al cambio climático
[@clarke2024wwa].

## Preguntas

1. ¿Qué tan excepcional fue la vaciante de 2024 frente a 38 años de registros?
2. ¿Con qué probabilidad se repetirá un nivel por debajo de 4 m?
3. ¿Qué relación tienen las vaciantes con la sequía local y con El Niño?
4. ¿Qué sistemas de la ciudad fallan y durante cuántos días?
5. ¿Qué proyectan los modelos para la sequía?

## Cadena de análisis

```{mermaid}
flowchart LR
  N[Nivel diario IDEAM] --> MN[Mínimos anuales] --> GEV[GEV de mínimos<br/>L-momentos]
  N --> D[Días bajo 6 m y 4 m]
  ERA[ERA5: lluvia y ET0] --> SPEI[SPI y SPEI]
  ONI[ONI NOAA] --> REL[Relación con El Niño]
  MN --> REL
  L[Landsat aguas bajas] --> AG[Agua frente a la ciudad]
  D --> SIS[Riesgo sistémico:<br/>navegación, agua, alimentos, salud]
  AG --> SIS
  CCKP[CMIP6 CCKP] --> ESC[SPEI-12, días secos, Tmax]
```

## Datos y métodos

Serie IDEAM [@ideam2026niveles]; GEV ajustada a los mínimos negados por L-momentos [@hosking1985]; SPI [@mckee1993] y
SPEI [@vicente2010spei] con ERA5 [@hersbach2020]; índice ONI de la NOAA; compuestos Landsat de aguas bajas con MNDWI
[@xu2006mndwi]; proyecciones del CCKP [@cckp2024].

## Limitaciones

- Los umbrales de 6 m y 4 m son **ilustrativos**: deben reemplazarse por los calados y niveles operativos de la
  Capitanía de Puerto y las empresas de transporte.
- La lluvia sobre Leticia explica solo una parte de la vaciante: el nivel depende de la lluvia en toda la cuenca
  alta (Perú, Ecuador, Colombia).
- Los impactos sistémicos (precios, días de racionamiento) no se registran de forma sistemática: la tabla de
  sistemas es cualitativa.
