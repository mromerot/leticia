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
  - Población repartida entre edificaciones (método dasimétrico)
* - Coberturas del suelo
  - ESA WorldCover 10 m 2021 [@zanaga2022worldcover]
  - Vegetación continua (interfaz urbano-forestal), área construida
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

## Vulnerabilidad

Sin datos abiertos de materiales de construcción, edad o ingreso por manzana, la vulnerabilidad se aproxima con un
índice de **densidad construida, población, cercanía al río y falta de vegetación** (pesos en `parametros.yaml`).
Las dos mejoras de mayor valor serían el catastro con el material de las cubiertas (vendavales, calor) y el censo
por manzana del DANE con edad y condiciones de vida.
