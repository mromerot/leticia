"""El paso de publicación convierte las salidas Markdown de los cuadernos en HTML."""
import importlib.util
import json
from pathlib import Path

import pytest

pytest.importorskip("markdown")
RAIZ = Path(__file__).resolve().parents[1]


def _modulo():
    spec = importlib.util.spec_from_file_location("salidas", RAIZ / "recursos_web" / "salidas_markdown_a_html.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_salida_markdown_pasa_a_html(tmp_path):
    nb = {"cells": [{"cell_type": "code", "source": "", "metadata": {}, "outputs": [
        {"output_type": "display_data", "metadata": {},
         "data": {"text/markdown": "Mínimo de 2024: **2.24 m**", "text/plain": "<IPython.core.display.Markdown object>"}}]}],
          "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    ruta = tmp_path / "c.ipynb"
    ruta.write_text(json.dumps(nb), encoding="utf-8")
    assert _modulo().convertir(ruta) == 1
    datos = json.loads(ruta.read_text(encoding="utf-8"))["cells"][0]["outputs"][0]["data"]
    assert datos == {"text/html": "<p>Mínimo de 2024: <strong>2.24 m</strong></p>"}
