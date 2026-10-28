---
title: Cómo ejecutar los cuadernos en Google Colab
short_title: Ejecutar en Colab
---

Todos los análisis de este libro son **cuadernos de Jupyter** (`.ipynb`) que se abren y ejecutan en
[Google Colab](https://colab.research.google.com) sin instalar nada.

## Paso a paso

1. Abra la página del cuaderno en este libro y haga clic en **Open in Colab** (o abra
   `https://colab.research.google.com/github/mromerot/leticia/blob/main/<ruta del cuaderno>`).
2. Ejecute todas las celdas (*Entorno de ejecución → Ejecutar todas*). La primera celda instala el paquete del
   proyecto desde GitHub:

   ```python
   import sys, subprocess
   if "google.colab" in sys.modules:
       subprocess.run([sys.executable, "-m", "pip", "install", "-q", "leticia @ git+https://github.com/mromerot/leticia"], check=True)
   from leticia.libro import preparar, intentar
   preparar()
   ```

   (En el libro publicado esa celda está oculta; en Colab aparece al inicio.)
3. Cada cuaderno descarga los datos que necesita desde sus fuentes oficiales y los guarda en
   `/content/datos_leticia/`. La primera ejecución de algunos cuadernos tarda varios minutos (imágenes Landsat y
   Sentinel-2, proyecciones CMIP6); las siguientes reutilizan la caché mientras la sesión siga abierta.

## Orden recomendado

```{list-table}
:header-rows: 1
* - Cuaderno
  - Tiempo aproximado de la primera ejecución
* - [2.6 Área de estudio](../02_datos/26_area_estudio.ipynb)
  - 5–10 min (mosaico Sentinel-2, edificaciones, población)
* - [1.7 Perfil de riesgos](../01_conceptos/17_perfil_riesgos.ipynb)
  - 1–3 min (DesInventar, UNGRD, ThinkHazard)
* - 3.x *b. Amenaza*
  - 1–5 min cada uno
* - 3.x *c. Riesgo*
  - 2–6 min cada uno (usan la malla de 2.6, que se crea sola si falta)
* - 3.x *d. Escenarios*
  - 2–8 min cada uno (lectura remota de las proyecciones del CCKP)
* - [3.7 Síntesis](../03_analisis/37_sintesis.ipynb)
  - 5–10 min si se ejecuta sola
```

## Si algo falla

- Si un servicio no responde (por ejemplo, la API de Open-Meteo limita las consultas), el cuaderno muestra un aviso
  en lugar de detenerse. Espere unos minutos y vuelva a ejecutar la celda.
- Para guardar los datos entre sesiones, monte Google Drive y defina la carpeta de datos antes de la primera celda:

  ```python
  import os
  from google.colab import drive
  drive.mount("/content/drive")
  os.environ["LETICIA_DATOS"] = "/content/drive/MyDrive/datos_leticia"
  ```

## Replicar en otra ciudad

Copie `src/leticia/config/` a una carpeta `config/` en su directorio de trabajo y edite `aoi.yaml` (nombre, código
DIVIPOLA, estación del IDEAM, extensiones), `sources.yaml` (fuentes) y `parametros.yaml` (umbrales y pesos). El
paquete usa esa configuración en lugar de la incluida.
