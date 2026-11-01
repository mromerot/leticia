# EVA — instrucciones para Claude Code

Proyecto: **EVA — Evaluación y análisis de riesgos de desastres**, libro reproducible cuya primera aplicación son los
**riesgos de desastres y climáticos de Leticia (Amazonas, Colombia)**, con la estructura de SIDRo
(https://mromerot.github.io/SIDRo/). Autor: Mauricio Romero. Idioma: **español**. El repositorio y el paquete
conservan el nombre `leticia`.

## Decisiones fijas
- Plataforma: **MyST** (`myst.yml`), publicada en GitHub Pages (rama `gh-pages`) por `.github/workflows/publicar.yml`.
- Todo el análisis en **cuadernos `.ipynb` compatibles con Google Colab**; la primera celda (etiqueta `remove-cell`)
  instala el paquete desde GitHub. Los cuadernos se ejecutan con datos reales y se versionan **con sus salidas**;
  la publicación no los vuelve a ejecutar (`jupyter: false`).
- Estructura: 1 Conceptos y evidencia (1.1–1.6 + cuaderno 1.7 de perfil de riesgos + 1.8 flujos de la literatura) ·
  2 Fuentes de datos (2.1–2.5 + cuaderno 2.6 de área de estudio) · 3 Análisis: 3.1 inundación, 3.2 sequía y estiaje,
  3.3 erosión, 3.4 calor, 3.5 incendios, 3.6 lluvias y vendavales, 3.7 dengue y clima (cada uno `index.md`,
  `a_descripcion.md`, `b_amenaza.ipynb`, `c_riesgo.ipynb`, `d_escenarios.ipynb` y `e_medidas.md`), 3.8 síntesis y 3.9 análisis multiamenaza (cuaderno único `39_multiamenaza.ipynb`: flujo de seis
  etapas de 1.1 con cadenas de detonantes, regla del máximo y bandas mínima/media/máxima; parámetros ilustrativos en `parametros.yaml`, sección `multiamenaza`).
- Medidas (`e_medidas.md`): se clasifican según la Ley 1523 (prevención, mitigación del riesgo, protección financiera;
  preparación y conocimiento cuando aplica) y se marca si son adaptación o tienen cobeneficio de mitigación del cambio
  climático (Ley 1931). Escribir siempre «mitigación del riesgo» o «mitigación del cambio climático» (ver 1.1).
- Paquete `src/leticia`; los cuadernos solo llaman sus funciones. Configuración en `src/leticia/config/*.yaml`
  (un `config/` en la carpeta de trabajo tiene prioridad). Nada del territorio va escrito en el código.
- Datos en `data/` (o `LETICIA_DATOS`; en Colab `/content/datos_leticia`), no se versionan.
- CRS de trabajo EPSG:9377; rásteres en EPSG:4326.
- Citas con `[@clave]` contra `references.bib`; citas del inglés = traducción propia; notas de prensa solo para
  hechos recientes, señaladas como tales. No inventar URL.
- Identidad visual en `recursos_web/eva/`: logo (la E son las tres capas del riesgo: río/amenaza, bosque/exposición,
  tierra/vulnerabilidad), favicon, íconos circulares de amenaza y `estilo.css` (tamaños de fuente de CCDR-tools,
  sidebar fijo desde 1024 px). Tras cambiar `estilo.css` o un ícono: `python recursos_web/eva/construir_css.py`
  (escribe `eva.css`). Las amenazas van en el primer nivel del `toc` de `myst.yml` para que el sidebar las muestre.
- Serie del IDEAM: se excluye 2007 (cambio del cero de la regla); extremos con GEV por L-momentos.

## Comandos
```bash
pip install -e ".[libro,dev]"
pytest && ruff check src tests
python -m leticia.catalogo          # regenera book/02_datos/25_catalogo.md
myst start                          # vista previa
myst build --html                   # sitio en _build/html
```
