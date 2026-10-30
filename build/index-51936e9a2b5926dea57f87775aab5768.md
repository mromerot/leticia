---
title: 3.7 Dengue y clima
short_title: 3.7 Dengue y clima
subtitle: Un riesgo para la salud que responde a la temperatura, el agua y la frontera
---

El dengue es el riesgo climático para la salud mejor documentado en Leticia. Este flujo se agregó a partir de la
[revisión de la literatura](../../01_conceptos/18_revision_literatura.md): describe los casos notificados al
SIVIGILA (2007–2022, vía OpenDengue), los compara con la ventana térmica de la transmisión por *Aedes aegypti*,
replica la evaluación de pronósticos hidroclimáticos de Beal et al. (2025) para Leticia y proyecta la aptitud
térmica con el ensamble CMIP6 del Banco Mundial.

**Resultados clave (ejecución del 28 de octubre de 2026 con datos reales):**

- Se notificaron **4.366 casos** entre 2007 y 2022; el brote de **2019** (1.716 casos) superó el percentil 75 de los
  años previos los doce meses. Los casos alcanzan su máximo en **octubre**, al final de la temporada menos lluviosa.
- Desde 2000, más de la mitad de los meses tiene una temperatura media dentro del rango de transmisión máxima
  (26–29 °C), frente a uno de cada tres en 1970–1999.
- Las señales climáticas con rezago son débiles (correlaciones menores de 0,25). Con los datos públicos, el
  pronóstico autorregresivo mejora mucho la climatología a 1 mes (habilidad 0,76) y algo a 3 meses (0,35); los
  modelos con temperatura, lluvia, humedad o TSM **no** la mejoran: no se reproduce el resultado de Beal et al.
- Con SSP1-2.6 y SSP2-4.5 los doce meses quedan en el rango de transmisión máxima; con SSP5-8.5 hacia 2080–2099 la
  temperatura media (~30,6 °C) supera el óptimo de 29,1 °C todo el año.

## Páginas del flujo

- [a. Descripción](a_descripcion.md)
- [b. Amenaza](b_amenaza.ipynb) [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mromerot/leticia/blob/main/book/03_analisis/37_dengue/b_amenaza.ipynb)
- [c. Riesgo](c_riesgo.ipynb) [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mromerot/leticia/blob/main/book/03_analisis/37_dengue/c_riesgo.ipynb)
- [d. Escenarios](d_escenarios.ipynb) [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mromerot/leticia/blob/main/book/03_analisis/37_dengue/d_escenarios.ipynb)
- [e. Medidas de reducción del riesgo, mitigación y adaptación](e_medidas.md)

Los cuadernos *b*, *c* y *d* se ejecutan en Google Colab con el botón de cada uno; las salidas publicadas aquí
provienen de su ejecución en la nube con datos reales.
