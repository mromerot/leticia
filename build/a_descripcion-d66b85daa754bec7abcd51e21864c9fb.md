---
title: 3.5.a Descripción — Incendios de cobertura vegetal y humo
short_title: a. Descripción
---

## La amenaza en Leticia

El bosque húmedo amazónico casi no arde de forma natural; el fuego llega con las quemas de rastrojos y potreros y la
deforestación, y escapa al bosque cuando la sequía seca la hojarasca. El Panel Científico por la Amazonía identifica
la **sinergia entre sequía, deforestación y fuego** como el principal riesgo para el bosque [@marengo2024spa], y
Flores et al. estiman que hasta la mitad del bosque podría enfrentar perturbaciones combinadas hacia 2050
[@flores2024]. En Leticia la UNGRD registró 14 incendios de cobertura vegetal en 2024, frente a uno o ninguno en años
anteriores [@ungrd2026emergencias].

## Preguntas

1. ¿Cuántos focos de calor hay, cuándo y dónde?
2. ¿Cuánto bosque se ha perdido alrededor de la ciudad?
3. ¿Qué edificaciones están en la interfaz urbano-forestal y cerca de focos recientes?
4. ¿Cómo cambiarán las condiciones que favorecen el fuego?

## Cadena de análisis

```{mermaid}
flowchart LR
  F[FIRMS MODIS y VIIRS] --> A[Focos por año y mes]
  H[Hansen GFC] --> D[Pérdida de bosque]
  ERA[ERA5] --> S[SPEI-3] --> R[Fuego vs. sequía]
  A --> R
  W[ESA WorldCover] --> I[Vegetación continua ≥ 10 ha] --> IF[Interfaz urbano-forestal]
  E[Edificaciones] --> IF
  F --> IF
  CCKP[CMIP6 CCKP] --> ESC[Condiciones de incendio futuras]
  D --> USO[Escenarios de deforestación]
```

## Datos y métodos

FIRMS MODIS y VIIRS [@giglio2016; @schroeder2014]; Global Forest Change [@hansen2013]; ESA WorldCover
[@zanaga2022worldcover]; ERA5 y SPEI [@hersbach2020; @vicente2010spei]; proyecciones del CCKP [@cckp2024].

## Limitaciones

- El archivo de FIRMS por país solo incluye Colombia: no hay focos de Brasil ni de Perú, que aportan humo.
- Los incendios pequeños de sotobosque y rastrojo escapan a sensores de 375 m–1 km.
- No hay un índice meteorológico de incendio calibrado para la Amazonía colombiana; se usa el balance hídrico.
