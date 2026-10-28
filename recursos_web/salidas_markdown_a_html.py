"""Convierte a HTML las salidas Markdown de los cuadernos antes de construir el sitio con MyST.

Los cuadernos muestran textos con `display(Markdown(...))`, que Colab y Jupyter presentan con formato. El tema web
de MyST, en cambio, muestra las salidas `text/markdown` como texto plano, con los asteriscos a la vista. Este paso,
que solo corre en la publicación (`.github/workflows/publicar.yml`), reemplaza cada salida `text/markdown` por su
equivalente `text/html`. Los cuadernos del repositorio no cambian.

Uso: python recursos_web/salidas_markdown_a_html.py book
"""
import json
import sys
from pathlib import Path

import markdown


def convertir(ruta: Path) -> int:
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    n = 0
    for celda in nb.get("cells", []):
        for salida in celda.get("outputs", []):
            datos = salida.get("data", {})
            if "text/markdown" not in datos:
                continue
            texto = datos.pop("text/markdown")
            texto = "".join(texto) if isinstance(texto, list) else texto
            datos["text/html"] = markdown.markdown(texto, extensions=["tables", "sane_lists"])
            datos.pop("text/plain", None)      # «<IPython.core.display.Markdown object>» no aporta nada en la web
            n += 1
    if n:
        ruta.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return n


if __name__ == "__main__":
    total = 0
    for raiz in sys.argv[1:] or ["book"]:
        for cuaderno in sorted(Path(raiz).rglob("*.ipynb")):
            total += convertir(cuaderno)
    print(f"salidas Markdown convertidas a HTML: {total}")
