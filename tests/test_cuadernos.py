"""Los cuadernos se publican con sus salidas (MyST no los vuelve a ejecutar): ninguno debe quedar vacío ni con errores."""
import json
from pathlib import Path

import pytest

CUADERNOS = sorted(Path(__file__).resolve().parents[1].joinpath("book").rglob("*.ipynb"))


@pytest.mark.parametrize("ruta", CUADERNOS, ids=lambda p: p.name if p.parent.name == "book" else f"{p.parent.name}/{p.name}")
def test_cuaderno_ejecutado_sin_errores(ruta):
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    codigo = [c for c in nb["cells"] if c["cell_type"] == "code"]
    salidas = [o for c in codigo for o in c.get("outputs", [])]
    assert salidas, f"{ruta.name} no tiene salidas: ejecútelo antes de publicar"
    assert not [o for o in salidas if o.get("output_type") == "error"], f"{ruta.name} tiene celdas con error"
    primera = nb["cells"][0]["source"]
    primera = "".join(primera) if isinstance(primera, list) else primera
    assert primera.startswith("---") and "colab.research.google.com" in primera
