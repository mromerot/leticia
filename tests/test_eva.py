"""La hoja de estilo de EVA está al día con su fuente y sus íconos, y cada ícono apunta a un flujo del libro."""
import importlib.util
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
EVA = RAIZ / "recursos_web" / "eva"


def _construir():
    spec = importlib.util.spec_from_file_location("construir_css", EVA / "construir_css.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_eva_css_generado_desde_su_fuente():
    mod = _construir()
    esperado = (EVA / "estilo.css").read_text(encoding="utf-8").replace("/* ICONOS */", mod.reglas())
    assert (EVA / "eva.css").read_text(encoding="utf-8") == esperado, "ejecute recursos_web/eva/construir_css.py"


def test_iconos_corresponden_a_flujos_del_indice():
    mod = _construir()
    toc = yaml.safe_load((RAIZ / "myst.yml").read_text(encoding="utf-8"))["project"]["toc"]
    archivos = [e.get("file", "") for e in toc]
    for slug, icono in mod.ICONOS.items():
        assert (EVA / "iconos" / f"{icono}.svg").exists()
        carpeta = slug.replace("-", "_")
        assert any(carpeta in a for a in archivos), f"{slug} no está en el primer nivel del índice"


def test_archivos_de_identidad_en_myst_yml():
    opciones = yaml.safe_load((RAIZ / "myst.yml").read_text(encoding="utf-8"))["site"]["options"]
    for clave in ("logo", "logo_dark", "favicon", "style"):
        assert (RAIZ / opciones[clave]).exists(), clave
