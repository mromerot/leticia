"""Escribe `eva.css`: la hoja de estilo de EVA con los íconos de amenaza incrustados como SVG.

Uso: `python recursos_web/eva/construir_css.py` (después de cambiar `estilo.css` o un ícono de `iconos/`).
Cada ícono se asocia al enlace del sidebar cuya ruta termina en `/analisis/<slug>`.
"""
from pathlib import Path
from urllib.parse import quote

AQUI = Path(__file__).parent

# slug de la página en el sitio -> archivo del ícono
ICONOS = {
    "inundacion": "inundacion",
    "sequia": "sequia",
    "erosion": "erosion",
    "calor": "calor",
    "incendios": "incendios",
    "lluvias-vendavales": "lluvias_vendavales",
    "dengue": "dengue",
    "sintesis": "sintesis",
}


def uri_svg(ruta: Path) -> str:
    svg = " ".join(ruta.read_text(encoding="utf-8").split())
    return "data:image/svg+xml," + quote(svg, safe=" =:/,';()-.")


def reglas() -> str:
    lineas = []
    selectores = ", ".join(f".myst-primary-sidebar a[href$='/analisis/{s}']" for s in ICONOS)
    lineas.append(f"{selectores} {{\n  display: flex;\n  align-items: center;\n  gap: 0.5rem;\n}}")
    lineas.append(
        ", ".join(f".myst-primary-sidebar a[href$='/analisis/{s}']::before" for s in ICONOS)
        + " {\n  content: \"\";\n  flex: none;\n  width: 1.45em;\n  height: 1.45em;\n"
        "  background: no-repeat center / contain;\n}"
    )
    for slug, archivo in ICONOS.items():
        uri = uri_svg(AQUI / "iconos" / f"{archivo}.svg")
        lineas.append(f".myst-primary-sidebar a[href$='/analisis/{slug}']::before {{ background-image: url(\"{uri}\"); }}")
    return "\n".join(lineas) + "\n"


if __name__ == "__main__":
    base = (AQUI / "estilo.css").read_text(encoding="utf-8")
    (AQUI / "eva.css").write_text(base.replace("/* ICONOS */", reglas()), encoding="utf-8")
    print("escrito", AQUI / "eva.css")
