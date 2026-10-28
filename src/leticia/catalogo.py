"""Genera la página 2.5 del libro (catálogo de fuentes) a partir de `config/sources.yaml`."""
from __future__ import annotations

from pathlib import Path

from .config import fuentes

SECCIONES = {"2.1": "Amenaza", "2.2": "Exposición y vulnerabilidad", "2.3": "Clima", "2.4": "Otros"}


def pagina() -> str:
    lineas = ["---", "title: 2.5 Catálogo de fuentes", "short_title: 2.5 Catálogo", "---", "",
              "Tabla generada automáticamente desde `config/sources.yaml` con `python -m leticia.catalogo`. Cada capa indica su",
              "nivel de respaldo, la entidad responsable, el producto, la resolución, la licencia y la fecha en que se verificó",
              "que el recurso responde desde la nube.", ""]
    for sec, nombre in SECCIONES.items():
        capas = {k: v for k, v in fuentes().items() if v["seccion"] == sec}
        if not capas:
            continue
        lineas += [f"## {sec} {nombre}", "", "```{list-table}", ":header-rows: 1",
                   "* - Capa", "  - Nivel", "  - Entidad y producto", "  - Escala", "  - Licencia", "  - Verificado"]
        for clave, c in capas.items():
            enlace = c.get("url_ficha") or c["url"]
            lineas += [f"* - **{c['tema']}** (`{clave}`)", f"  - {c['nivel']}",
                       f"  - {c['entidad']}: {c['producto']} ([enlace]({enlace}))",
                       f"  - {c.get('escala', '')}", f"  - {c.get('licencia', '')}", f"  - {c.get('verificado') or 'pendiente'}"]
        lineas += ["```", ""]
    return "\n".join(lineas)


def generar(destino: str | Path = "book/02_datos/25_catalogo.md") -> Path:
    destino = Path(destino)
    destino.write_text(pagina(), encoding="utf-8")
    return destino


if __name__ == "__main__":
    print(generar())
