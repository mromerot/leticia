"""Mapas y gráficas con un estilo común para todo el libro."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

from .config import aoi_cfg, fuentes

# Paleta del libro
AZUL_RIO = "#1f6f9f"
TIERRA = "#a6611a"
CALOR = "#c2410c"
VERDE = "#2e7d32"
GRIS = "#5f6b76"
ROJO = "#b2182b"
ESCENARIOS = {"ssp126": "#1b9e77", "ssp245": "#e6ab02", "ssp370": "#d95f02", "ssp585": "#b2182b", "historico": "#4d4d4d"}
NOMBRE_ESC = {"ssp126": "SSP1-2.6", "ssp245": "SSP2-4.5", "ssp370": "SSP3-7.0", "ssp585": "SSP5-8.5"}


def estilo() -> None:
    plt.rcParams.update({
        "figure.dpi": 100, "savefig.dpi": 100, "figure.figsize": (9, 4.2), "axes.spines.top": False,
        "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25, "axes.titlesize": 11,
        "axes.titleweight": "bold", "axes.labelsize": 10, "legend.fontsize": 8.5, "legend.frameon": False,
        "font.family": "DejaVu Sans",
    })


def nota_fuente(*capas: str) -> str:
    """Texto de atribución a partir del catálogo de fuentes."""
    partes = []
    for c in capas:
        f = fuentes()[c]
        partes.append(f"{f['entidad']} — {f['producto']}")
    return "Fuente: " + "; ".join(partes) + "."


def fondo(ax, clave_bbox: str = "bbox_urbano", alfa: float = 1.0) -> None:
    """Pinta el mosaico Sentinel-2 como mapa base (en EPSG:4326) si está disponible."""
    try:
        from .espacial import mosaico_rgb
        from .fuentes import bbox

        rgb = mosaico_rgb()
        b = bbox(clave_bbox)
        sub = rgb.sel(x=slice(b[0], b[2]), y=slice(b[3], b[1]))
        img = np.clip(np.nan_to_num(np.moveaxis(sub.values, 0, -1)), 0, 255).astype("uint8")
        ax.imshow(img, extent=(float(sub.x.min()), float(sub.x.max()), float(sub.y.min()), float(sub.y.max())),
                  alpha=alfa, zorder=0, interpolation="bilinear")
    except Exception as e:  # noqa: BLE001
        ax.set_facecolor("#e9ecef")
        ax.text(0.01, 0.01, f"(sin mapa base: {type(e).__name__})", transform=ax.transAxes, fontsize=7, color=GRIS)


def marco(ax, clave_bbox: str = "bbox_urbano", titulo: str | None = None) -> None:
    from .fuentes import bbox

    b = bbox(clave_bbox)
    ax.set_xlim(b[0], b[2])
    ax.set_ylim(b[1], b[3])
    ax.set_aspect(1 / np.cos(np.radians((b[1] + b[3]) / 2)))
    ax.tick_params(labelsize=7)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.grid(False)
    if titulo:
        ax.set_title(titulo)
    # flecha de norte y escala aproximada
    ax.annotate("N", xy=(0.95, 0.93), xytext=(0.95, 0.83), xycoords="axes fraction", ha="center", fontsize=9,
                fontweight="bold", arrowprops=dict(arrowstyle="-|>", color="k", lw=1.2))
    km = 1 / (111.32 * np.cos(np.radians((b[1] + b[3]) / 2)))
    largo = 1 if (b[2] - b[0]) < 0.2 else 5
    x0, y0 = b[0] + 0.04 * (b[2] - b[0]), b[1] + 0.04 * (b[3] - b[1])
    ax.plot([x0, x0 + largo * km], [y0, y0], color="k", lw=3, solid_capstyle="butt")
    ax.text(x0 + largo * km / 2, y0 + 0.015 * (b[3] - b[1]), f"{largo} km", ha="center", fontsize=7)


def mapa_celdas(m, columna: str, ax=None, cmap: str = "magma_r", titulo: str | None = None, etiqueta: str | None = None,
                categorias: list[str] | None = None, colores: list[str] | None = None, alfa: float = 0.75,
                con_fondo: bool = True, clave_bbox: str = "bbox_urbano", **kw):
    """Mapa de la malla coloreada por una columna continua o categórica, sobre el mosaico Sentinel-2."""
    if ax is None:
        _, ax = plt.subplots(figsize=(6.2, 7))
    if con_fondo:
        fondo(ax, clave_bbox)
    g = m.to_crs(4326)
    if categorias:
        colores = colores or plt.get_cmap(cmap, len(categorias)).colors
        for cat, col in zip(categorias, colores):
            sub = g[g[columna] == cat]
            if len(sub):
                sub.plot(ax=ax, color=col, alpha=alfa, linewidth=0, zorder=2)
        ax.legend(handles=[Patch(color=c, label=k) for k, c in zip(categorias, colores)], loc="lower right",
                  fontsize=7.5, frameon=True, title=etiqueta, title_fontsize=8)
    else:
        g.dropna(subset=[columna]).plot(column=columna, ax=ax, cmap=cmap, alpha=alfa, linewidth=0, legend=True, zorder=2,
                                        legend_kwds={"shrink": 0.6, "label": etiqueta or columna}, **kw)
    marco(ax, clave_bbox, titulo)
    return ax


def pie(texto: str) -> None:
    """Pie de figura con la fuente (se imprime como texto en cursiva bajo la figura)."""
    from IPython.display import Markdown, display

    display(Markdown(f"*{texto}*"))


def leyenda_puntos(ax, gdf, etiqueta: str = "nombre", color: str = "k") -> None:
    g = gdf.to_crs(4326)
    ax.scatter(g.geometry.x, g.geometry.y, s=18, c=color, marker="^", zorder=5, edgecolor="white", linewidth=0.6)
    for _, r in g.iterrows():
        ax.annotate(r[etiqueta], (r.geometry.x, r.geometry.y), xytext=(4, 3), textcoords="offset points", fontsize=7,
                    zorder=6, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7))


def tabla_bonita(df: pd.DataFrame, decimales: int = 1):
    return df.style.format(precision=decimales, thousands=".", decimal=",")


def centro() -> tuple[float, float]:
    c = aoi_cfg()["centro"]
    return c["lon"], c["lat"]


def _rotulos(ax, rotulos: list[dict], color: str = "k", **kw) -> None:
    for r in rotulos:
        estilo_r = dict(color=AZUL_RIO if r.get("rio") else color, fontsize=kw.get("fontsize", 9), ha="center", va="center",
                        rotation=r.get("rotacion", 0), style="italic" if r.get("rio") else "normal",
                        fontweight="bold" if r.get("ciudad") or r.get("municipio") else "normal", zorder=7)
        ax.text(r["lon"], r["lat"], r["texto"], **{**estilo_r, **kw.get("sobre", {})})


def _rectangulo(ax, b, color: str, lw: float = 1.4) -> None:
    from matplotlib.patches import Rectangle

    ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fill=False, ec=color, lw=lw, zorder=6))


def mapa_localizacion():
    """Mapa del área de estudio en tres escalas: norte de Suramérica, municipio en la triple frontera y entorno de la
    ciudad sobre Sentinel-2. Extensiones y rótulos en la sección `mapa` de `aoi.yaml`."""
    from matplotlib.colors import ListedColormap
    from matplotlib.lines import Line2D

    from .aoi import area_urbana
    from .fuentes import bbox, limite_municipal, municipios, natural_earth, raster_estatico

    cfg = aoi_cfg()
    m = cfg["mapa"]
    paises, rios = natural_earth("paises"), natural_earth("rios_principales")
    rios = rios[rios["featurecla"].str.contains("River") & (rios["scalerank"] <= 6)]
    mun = limite_municipal()
    vecinos = municipios("bbox_municipio")
    urbana = area_urbana().to_crs(4326)
    agua = raster_estatico("jrc-gsw", "occurrence", "bbox_municipio", resolucion=0.0009)
    b_ctx, b_mun, b_reg = m["contexto"], bbox("bbox_municipio"), bbox("bbox_regional")
    tierra, propio, borde = "#f1efe9", "#dcebd5", "#8c8c8c"

    fig, ax = plt.subplots(1, 3, figsize=(12.5, 4.4), gridspec_kw={"width_ratios": [1.0, 0.9, 1.3]})

    # (a) contexto continental
    ax[0].set_facecolor("#dcecf5")
    paises.plot(ax=ax[0], color=tierra, edgecolor=borde, lw=0.5)
    paises[paises["iso_a3"] == cfg["pais"]].plot(ax=ax[0], color=propio, edgecolor="#4d4d4d", lw=0.8)
    rios.plot(ax=ax[0], color=AZUL_RIO, lw=0.7, alpha=0.8)
    _rectangulo(ax[0], b_mun, ROJO)
    ax[0].annotate(cfg["nombre"], ((b_mun[0] + b_mun[2]) / 2, b_mun[1]), xytext=(0, -9), textcoords="offset points",
                   ha="center", va="top", fontsize=9.5, fontweight="bold", color=ROJO)
    _rotulos(ax[0], m["rotulos_contexto"], color="#4d4d4d")
    ax[0].set_title("a. Norte de Suramérica")

    # (b) municipio en la triple frontera
    ax[1].set_facecolor(tierra)
    vecinos.plot(ax=ax[1], color=propio, edgecolor=borde, lw=0.6)
    mun.plot(ax=ax[1], color="#b9d8ad", edgecolor="k", lw=1.0)
    ax[1].imshow(np.where(agua.values >= 50, 1, np.nan), cmap=ListedColormap([AZUL_RIO]), interpolation="nearest",
                 extent=(float(agua.x.min()), float(agua.x.max()), float(agua.y.min()), float(agua.y.max())), zorder=3)
    urbana.plot(ax=ax[1], color=ROJO, zorder=5)
    _rectangulo(ax[1], b_reg, "k", lw=1.2)
    for _, r in vecinos.iterrows():
        x, y = _centro_rotulo(r.geometry.intersection(_caja(b_mun)))
        propio_mun = r["shapeName"].casefold() == cfg["municipio"].casefold()
        ax[1].text(x, y, r["shapeName"] if propio_mun else r["shapeName"].replace(" ", "\n"), ha="center", va="center",
                   fontsize=9.5 if propio_mun else 7.5,
                   fontweight="bold" if propio_mun else "normal", color="#1f1f1f" if propio_mun else "#4d4d4d", zorder=6)
    _rotulos(ax[1], m["rotulos_municipio"], color="#4d4d4d", fontsize=9)
    ax[1].set_title("b. Municipio en la triple frontera")

    # (c) entorno de la ciudad
    fondo(ax[2], "bbox_regional")
    urbana.boundary.plot(ax=ax[2], color="yellow", lw=1.4, zorder=4)
    mun.boundary.plot(ax=ax[2], color="white", lw=0.9, ls="--", zorder=4)
    est = cfg["estacion_nivel"]
    ax[2].scatter(est["lon"], est["lat"], marker="^", s=55, c=AZUL_RIO, edgecolor="white", lw=0.8, zorder=6)
    _rotulos(ax[2], m["rotulos_regional"], sobre={"color": "white"})
    marco(ax[2], "bbox_regional", "c. Ciudad y río (Sentinel-2, temporada seca)")
    ax[2].legend(handles=[Line2D([], [], color="yellow", lw=1.4, label="Área urbana de análisis"),
                          Line2D([], [], color="white", lw=0.9, ls="--", label="Límite municipal"),
                          Line2D([], [], marker="^", ls="", mfc=AZUL_RIO, mec="white", ms=8,
                                 label=f"Estación hidrológica {est['nombre']} (IDEAM)")],
                 loc="upper left", fontsize=8, frameon=True, facecolor="white", framealpha=0.85)

    for a, bb in ((ax[0], b_ctx), (ax[1], b_mun)):
        a.set_xlim(bb[0], bb[2])
        a.set_ylim(bb[1], bb[3])
        a.set_aspect(1 / np.cos(np.radians((bb[1] + bb[3]) / 2)))
        a.tick_params(labelsize=7)
        a.set_xlabel("")
        a.set_ylabel("")
        a.grid(False)
    fig.tight_layout()
    return fig


def _caja(b):
    from shapely.geometry import box

    return box(*b)


def _centro_rotulo(geom) -> tuple[float, float]:
    """Punto interior más alejado del borde (polo de inaccesibilidad) de la parte más grande del polígono."""
    from shapely.ops import polylabel

    if geom.geom_type == "MultiPolygon":
        geom = max(geom.geoms, key=lambda g: g.area)
    return polylabel(geom, tolerance=0.005).coords[0]
