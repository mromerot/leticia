---
title: 2. Fuentes de datos
short_title: 2. Fuentes de datos
---

Esta sección describe los datos que usa el libro. Como en SIDRo, se agrupan en **amenaza**, **exposición y
vulnerabilidad**, **clima** y **otros**, y cada capa declara su nivel de respaldo (local, nacional o global), su
entidad responsable, su licencia y la fecha en que se verificó que el recurso responde ([2.5 Catálogo](25_catalogo.md)).
Todas las capas son **abiertas** y se descargan desde los cuadernos; ninguna requiere registro ni claves de acceso.

```{list-table}
:header-rows: 1
* - Página
  - Contenido
* - [2.1 Amenaza](21_amenaza.md)
  - Nivel del río (IDEAM), caudal (GloFAS), mapas de inundación (JRC), agua superficial (JRC GSW), focos de calor
    (FIRMS), pérdida de bosque (Hansen), registros de desastres (DesInventar, UNGRD) y ThinkHazard
* - [2.2 Exposición y vulnerabilidad](22_exposicion.md)
  - Límite municipal (DANE), edificaciones (Microsoft), población (Kontur), coberturas (ESA WorldCover), modelo de
    superficie (Copernicus) e infraestructura (OpenStreetMap)
* - [2.3 Clima](23_clima.md)
  - Serie diaria ERA5 (Open-Meteo) y proyecciones CMIP6 del CCKP (Banco Mundial)
* - [2.4 Otros datos](24_otros.md)
  - Índice ONI, catálogo de estaciones del IDEAM, imágenes Landsat y Sentinel-2
* - [2.5 Catálogo](25_catalogo.md)
  - Tabla generada desde `config/sources.yaml`
* - [2.6 Área de estudio (cuaderno)](26_area_estudio.ipynb)
  - Construye las capas base de exposición
```

:::{note} Lo que falta
Para Leticia no hay en datos abiertos estudios municipales de amenaza, catastro con materiales de construcción ni
censo por manzana descargable de forma automática. El libro lo compensa con productos nacionales y globales, y
señala en cada flujo qué dato local mejoraría más el resultado.
:::
