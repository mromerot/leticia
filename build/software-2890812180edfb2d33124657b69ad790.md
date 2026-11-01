---
title: Software
short_title: Software
---

El libro se construye con software libre:

```{list-table}
:header-rows: 1
* - Herramienta
  - Uso
* - [MyST / Jupyter Book 2](https://mystmd.org)
  - Construcción del libro y del sitio web
* - [Jupyter](https://jupyter.org) y [Google Colab](https://colab.research.google.com)
  - Cuadernos ejecutables
* - Paquete `leticia` (este repositorio)
  - Conectores de datos, hidrología, clima, procesamiento espacial, exposición, riesgo y mapas
* - pandas, NumPy, SciPy
  - Series de tiempo, estadística de extremos y tendencias
* - GeoPandas, Shapely, rasterio, rioxarray, xarray, scikit-image
  - Procesamiento vectorial y ráster
* - pystac-client, planetary-computer, odc-stac
  - Acceso a Landsat, Sentinel-2, JRC GSW, ESA WorldCover y Copernicus DEM en Microsoft Planetary Computer
* - netCDF4
  - Lectura remota (por rangos HTTP) de las proyecciones CMIP6 del CCKP
* - thermofeel (ECMWF) y SPEI
  - Estrés térmico (UTCI) y control de calidad del SPI
* - [CLIMADA](https://climada.ethz.ch)
  - Pérdida anual esperada por inundación y evaluación de medidas (3.1.c)
* - Matplotlib
  - Gráficas y mapas
```

## Instalar CLIMADA

CLIMADA (opcional, solo para la sección 2 de [3.1.c](../03_analisis/31_inundacion/c_riesgo.ipynb)) necesita la
biblioteca GDAL del sistema y, hoy, Python 3.10–3.12. En Colab el cuaderno la instala solo. En Linux:

```bash
sudo apt-get install -y libgdal-dev
pip install "gdal==$(gdal-config --version)" -e ".[climada]"
```

CLIMADA debe importarse antes que rasterio, porque ambos cargan su propia copia de GDAL; el cuaderno 3.1.c lo hace
en su primera celda.

## Estructura del repositorio

```
myst.yml, index.md           configuración y portada del libro
book/01_conceptos/           Sección 1: conceptos, contexto, evidencia y perfil de riesgos
book/02_datos/               Sección 2: fuentes de datos, catálogo y área de estudio
book/03_analisis/            Sección 3: siete flujos (a–e) y síntesis
book/recursos/               Colab, glosario, software, preguntas frecuentes, cómo citar
src/leticia/                 paquete de Python
src/leticia/config/          aoi.yaml, sources.yaml, parametros.yaml
tests/                       pruebas con datos sintéticos (sin red)
```

## Comandos

```bash
pip install -e ".[libro,dev]"     # paquete, Jupyter y herramientas de prueba
pytest                            # pruebas sin red
python -m leticia.catalogo        # regenera book/02_datos/25_catalogo.md
myst start                        # vista previa local del libro
myst build --html                 # sitio estático en _build/html
```
