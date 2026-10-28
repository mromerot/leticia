from leticia.config import aoi_cfg, fuentes, parametros


def test_configuracion_completa():
    a = aoi_cfg()
    assert a["codigo_divipola"] == "91001"
    assert {"bbox_urbano", "bbox_rio", "bbox_regional"} <= set(a)
    f = fuentes()
    for capa in ("nivel_rio_leticia", "caudal_glofas", "proyecciones_cckp", "edificaciones", "desinventar"):
        assert capa in f and f[capa]["url"].startswith("http")
    assert parametros()["hidrologia"]["periodos_excluidos"]
