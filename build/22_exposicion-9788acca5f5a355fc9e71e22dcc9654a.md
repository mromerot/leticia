---
title: 2.2 Datos de exposición y vulnerabilidad
short_title: 2.2 Exposición
---

```{list-table}
:header-rows: 1
* - Capa
  - Fuente
  - Uso en el libro
* - Límite municipal
  - DANE, Marco Geoestadístico Nacional (vía geoBoundaries)
  - Recortar el área urbana de análisis y separar Leticia de Tabatinga
* - Huellas de edificaciones
  - Microsoft Global ML Building Footprints [@microsoft2023buildings]
  - Exposición por edificación; área construida por celda
* - Población
  - Kontur Population (hexágonos H3 de ~0,7 km²) [@kontur2023]
  - Población repartida entre edificaciones (método dasimétrico); asentamientos rurales y ribereños fuera del casco urbano (3.2.c)
* - Coberturas del suelo
  - ESA WorldCover 10 m 2021 [@zanaga2022worldcover]
  - Vegetación continua (interfaz urbano-forestal), área construida
* - Coberturas de la tierra 2002–2024
  - SINCHI, SIAT-AC: Corine Land Cover 1:100.000 [@sinchi2026siatac]
  - Contraste de la interfaz urbano-forestal (3.5.c); cambio de coberturas alrededor de la ciudad (3.5.d)
* - Rondas hídricas y ecosistemas
  - SINCHI, SIAT-AC: áreas prioritarias de restauración en rondas hídricas y ecosistemas, 2024 [@sinchi2026siatac]
  - Planicie aluvial y drenajes priorizados, ecosistemas acuáticos de aguas blancas y negras (3.3.c)
* - Modelo digital de superficie
  - Copernicus DEM GLO-30 [@copernicusdem2021]
  - Altura sobre el río (aproximación HAND) y depresiones topográficas
* - Infraestructura de referencia
  - OpenStreetMap (Nominatim)
  - Hospital, aeropuerto, muelle, malecón, universidad
```

## Población dasimétrica

Kontur estima la población en hexágonos a partir de GHSL, Meta HRSL, Microsoft Buildings y otras fuentes. El libro
la reparte entre las edificaciones de cada hexágono en proporción al área de su huella y, en la frontera con
Tabatinga, conserva solo la fracción del hexágono que cae en Colombia. El resultado (~46 500 personas en la malla
urbana) es consistente con las proyecciones del DANE para la cabecera y sirve para **ordenar** las celdas por
población, no para contar personas.

## Coberturas, rondas y ecosistemas del SINCHI

El SINCHI cartografía las coberturas de la Amazonia colombiana con la leyenda Corine Land Cover adaptada a Colombia,
a escala 1:100.000, para 2002, 2007, 2012 y cada dos años desde 2014. Es la fuente oficial para medir el cambio del
paisaje alrededor de Leticia; frente a WorldCover (10 m) agrupa la ciudad y sus parches verdes en una sola unidad
y no ve los rastrojos pequeños. Tres precauciones:

- La capa de 2024 trae solo la leyenda agrupada y trata distinto las superficies de agua, así que las tasas de
  cambio se calculan hasta 2022.
- La capa de 2023 se publica con «derechos de autor» y no como dato abierto; no se usa.
- Las **áreas prioritarias de restauración en rondas hídricas** combinan una unidad geomorfológica (planicie
  aluvial, drenaje sencillo o doble) con su cobertura. La planicie aluvial no es una zona de inundación, y a
  1:100.000 no sirve para delimitar la ronda dentro de la ciudad.

## Vulnerabilidad

Sin datos abiertos de materiales de construcción, edad o ingreso por manzana, la vulnerabilidad se aproxima con un
índice de **densidad construida, población, cercanía al río y falta de vegetación** (pesos en `parametros.yaml`).
Las dos mejoras de mayor valor serían el catastro con el material de las cubiertas (vendavales, calor) y el censo
por manzana del DANE con edad y condiciones de vida.
