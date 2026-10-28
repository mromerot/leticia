"""Conectores de descarga con caché local.

Cada función descarga una capa del catálogo (`config/sources.yaml`), la guarda en
`data/processed/` y la devuelve. La segunda vez lee la copia local. Ninguna URL va fija en el
código de los cuadernos: todas salen del catálogo, de modo que la página 2.5 del libro y el
código citan la misma fuente.
"""
from __future__ import annotations

import gzip
import io
import json
import logging
import math
import os
import shutil
import time
from datetime import date
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from shapely.geometry import box, shape

from .config import aoi_cfg, dir_datos, fuentes

log = logging.getLogger(__name__)
SESION = requests.Session()
SESION.headers["User-Agent"] = "leticia-riesgos/0.1 (proyecto academico; github.com/mromerot/leticia)"
TIEMPO = 180

os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif,.tiff,.TIF")
os.environ.setdefault("GDAL_HTTP_MAX_RETRY", "4")
os.environ.setdefault("GDAL_HTTP_RETRY_DELAY", "2")


# ------------------------------------------------------------------ utilidades
def url(capa: str) -> str:
    return fuentes()[capa]["url"]


def ruta(nombre: str) -> Path:
    return dir_datos() / "processed" / nombre


def _get(u: str, params: dict | None = None, intentos: int = 8, **kw) -> requests.Response:
    """GET con reintentos y espera exponencial (las API públicas limitan la tasa de consultas).

    Ante un HTTP 429 (límite de consultas, frecuente en Open-Meteo desde IP compartidas) respeta la cabecera
    Retry-After y espera hasta 90 s entre intentos; en total puede esperar unos 5 minutos antes de fallar.
    """
    espera = 3
    tiempo = kw.pop("timeout", TIEMPO)
    for i in range(intentos):
        try:
            r = SESION.get(u, params=params, timeout=tiempo, **kw)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"HTTP {r.status_code}", response=r)
            r.raise_for_status()
            return r
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            resp = getattr(e, "response", None)
            if i == intentos - 1 or (resp is not None and resp.status_code not in (429, 500, 502, 503, 504)):
                raise
            pausa = espera
            if resp is not None and resp.status_code == 429:
                try:
                    pausa = max(pausa, float(resp.headers.get("Retry-After", 0)))
                except ValueError:
                    pass
            log.info("reintento %d de %s en %.0f s (%s)", i + 1, u, pausa, e)
            time.sleep(min(pausa, 90))
            espera = min(espera * 2, 90)
    raise RuntimeError("inalcanzable")


def descargar(u: str, destino: Path, forzar: bool = False) -> Path:
    """Descarga un archivo a `data/raw/` (sin volver a bajarlo si ya existe)."""
    destino = Path(destino)
    if destino.exists() and destino.stat().st_size > 0 and not forzar:
        return destino
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(destino.suffix + ".part")
    with SESION.get(u, stream=True, timeout=TIEMPO) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for bloque in r.iter_content(1 << 20):
                f.write(bloque)
    tmp.replace(destino)
    return destino


def _github_crudo(u: str) -> str:
    """Las descargas `github.com/<o>/<r>/raw/<sha>/<ruta>` de archivos LFS se sirven desde media.githubusercontent.com."""
    if "github.com/" in u and "/raw/" in u:
        dueno_repo, resto = u.split("github.com/")[1].split("/raw/")
        return f"https://media.githubusercontent.com/media/{dueno_repo}/{resto}"
    return u


def cache(nombre: str, fn, forzar: bool = False):
    """Lee `data/processed/<nombre>` si existe; si no, ejecuta `fn()` y guarda su resultado."""
    p = ruta(nombre)
    if p.exists() and not forzar:
        return leer(p)
    obj = fn()
    guardar(obj, p)
    return leer(p) if p.suffix in (".tif", ".parquet") else obj


def guardar(obj, p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix == ".parquet":
        obj.to_parquet(p)
    elif p.suffix == ".csv":
        obj.to_csv(p)
    elif p.suffix == ".json":
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    elif p.suffix == ".tif":
        obj.rio.to_raster(p, compress="deflate")
    else:
        raise ValueError(p.suffix)


def leer(p: Path):
    if p.suffix == ".parquet":
        try:
            return gpd.read_parquet(p)
        except (ValueError, TypeError):
            return pd.read_parquet(p)
    if p.suffix == ".csv":
        df = pd.read_csv(p, index_col=0)
        try:
            df.index = pd.to_datetime(df.index)
        except (ValueError, TypeError):
            pass
        return df.iloc[:, 0] if df.shape[1] == 1 and df.columns[0] in ("valor", "nivel_cm", "caudal_m3s") else df
    if p.suffix == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    if p.suffix == ".tif":
        import rioxarray  # noqa: F401
        import xarray as xr

        return xr.open_dataarray(p, engine="rasterio").squeeze(drop=True).load()
    raise ValueError(p.suffix)


def bbox(clave: str = "bbox_urbano", bufer_grados: float = 0.0) -> tuple[float, float, float, float]:
    b = aoi_cfg()[clave]
    return (b[0] - bufer_grados, b[1] - bufer_grados, b[2] + bufer_grados, b[3] + bufer_grados)


# ------------------------------------------------------------------ IDEAM
def nivel_rio(variable: str = "NV_MEDIA_D", codigo: str | None = None, forzar: bool = False,
              con_aprobacion: bool = False) -> pd.Series | pd.DataFrame:
    """Serie diaria de nivel (cm) de una estación del IDEAM desde su repositorio público S3.

    variable: NV_MEDIA_D (medio), NV_MN_D (mínimo), NV_MX_D (máximo). Con `con_aprobacion=True`
    devuelve también la columna `aprobacion`, que distingue datos definitivos de preliminares.
    """
    codigo = codigo or aoi_cfg()["estacion_nivel"]["codigo"]

    def _bajar():
        u = f"{url('nivel_rio_leticia')}/{variable}/{codigo}-{variable}.csv"
        df = pd.read_csv(io.StringIO(_get(u).text), parse_dates=["fechaObservacion"])
        df = df.rename(columns={"fechaObservacion": "fecha", "valorObservado": "nivel_cm", "nivelAprobacion": "aprobacion"})
        return df.set_index("fecha").sort_index()[["nivel_cm", "aprobacion"]]

    df = cache(f"ideam_{codigo}_{variable}.csv", _bajar, forzar)
    if con_aprobacion:
        return df
    s = df["nivel_cm"].astype(float)
    s.name = "nivel_cm"
    return s


def estaciones_ideam(municipio: str | None = None) -> pd.DataFrame:
    municipio = municipio or aoi_cfg()["municipio"]

    def _bajar():
        r = _get(url("estaciones_ideam"), params={"$where": f"municipio='{municipio}'", "$limit": 500})
        df = pd.DataFrame(r.json()).drop(columns=["ubicaci_n"], errors="ignore").drop_duplicates("codigo")
        return df.set_index("codigo")

    return cache(f"estaciones_ideam_{municipio}.csv", _bajar)


# ------------------------------------------------------------------ UNGRD
_CAMPOS_UNGRD = {
    "fallecidos": ["fallecidos", "muertos"],
    "heridos": ["heridos"],
    "personas": ["personas"],
    "familias": ["familias"],
    "viviendas_destruidas": ["viviendas_destruidas", "viv_destru"],
    "viviendas_averiadas": ["viviendas_averiadas", "viv_aver"],
    "hectareas": ["hectareas"],
}


def _numero(v) -> float:
    try:
        return float(str(v).replace(",", "").replace("$", "").strip() or 0)
    except ValueError:
        return np.nan


def emergencias_ungrd(municipio: str | None = None, forzar: bool = False) -> pd.DataFrame:
    """Emergencias del municipio reportadas a la UNGRD, armonizadas a partir de varios conjuntos anuales."""
    municipio = (municipio or aoi_cfg()["municipio"]).upper()
    cfg = fuentes()["emergencias_ungrd"]

    def _bajar():
        filas = []
        for cid in cfg["conjuntos"]:
            r = _get(f"{cfg['url']}/{cid}.json", params={"$limit": 5000, "$where": f"upper(municipio) like '%{municipio}%'"})
            for x in r.json():
                fila = {"fecha": x.get("fecha"), "evento": (x.get("evento") or "").strip().upper(), "conjunto": cid}
                for campo, alias in _CAMPOS_UNGRD.items():
                    fila[campo] = next((_numero(x[a]) for a in alias if a in x), np.nan)
                filas.append(fila)
        df = pd.DataFrame(filas)
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.tz_localize(None)
        df = df.dropna(subset=["fecha"]).drop_duplicates(subset=["fecha", "evento", "personas", "familias"])
        return df.sort_values("fecha").set_index("fecha")

    return cache(f"ungrd_emergencias_{municipio.lower()}.csv", _bajar, forzar)


# ------------------------------------------------------------------ DesInventar
_CAMPOS_DI = ["serial", "level1", "name1", "evento", "lugar", "fechano", "fechames", "fechadia", "muertos", "heridos",
              "desaparece", "afectados", "damnificados", "evacuados", "vivdest", "vivafec", "nhectareas", "fuentes", "di_comments"]


def desinventar(divipola: str | None = None, forzar: bool = False) -> pd.DataFrame:
    """Registros históricos de DesInventar Colombia para un municipio (código DIVIPOLA).

    El archivo de exportación nacional (~16 MB comprimido, ~550 MB de XML) se recorre en flujo y solo se
    conservan las fichas del municipio.
    """
    import xml.etree.ElementTree as ET
    import zipfile

    divipola = divipola or aoi_cfg()["codigo_divipola"]

    def _bajar():
        z = descargar(url("desinventar"), dir_datos() / "raw" / "DI_export_col.zip")
        filas = []
        with zipfile.ZipFile(z) as zf:
            nombre = next(n for n in zf.namelist() if n.endswith(".xml"))
            with zf.open(nombre) as fh:
                en_fichas = False
                for evento, elem in ET.iterparse(fh, events=("start", "end")):
                    if evento == "start" and elem.tag == "fichas":
                        en_fichas = True
                    elif evento == "end" and elem.tag == "TR":
                        if en_fichas and elem.findtext("level1") == divipola:
                            filas.append({c: elem.findtext(c) for c in _CAMPOS_DI})
                        elem.clear()
                    elif evento == "end" and elem.tag == "fichas":
                        break
        df = pd.DataFrame(filas)
        for c in ["muertos", "heridos", "desaparece", "afectados", "damnificados", "evacuados", "vivdest", "vivafec", "nhectareas"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        mes = pd.to_numeric(df["fechames"], errors="coerce").fillna(1).clip(1, 12).astype(int)
        dia = pd.to_numeric(df["fechadia"], errors="coerce").fillna(1).clip(1, 28).astype(int)
        df["fecha"] = pd.to_datetime(dict(year=pd.to_numeric(df["fechano"], errors="coerce"), month=mes, day=dia), errors="coerce")
        return df.dropna(subset=["fecha"]).set_index("fecha").sort_index()

    return cache(f"desinventar_{divipola}.csv", _bajar, forzar)


# ------------------------------------------------------------------ ThinkHazard
def thinkhazard() -> pd.DataFrame:
    def _bajar():
        datos = _get(url("thinkhazard")).json()
        return pd.DataFrame([{
            "codigo": h["hazardtype"]["mnemonic"], "amenaza": h["hazardtype"]["hazardtype"],
            "nivel": h["hazardlevel"]["title"], "nivel_cod": h["hazardlevel"]["mnemonic"]} for h in datos]).set_index("codigo")

    return cache("thinkhazard.csv", _bajar)


# ------------------------------------------------------------------ Open-Meteo (ERA5 y GloFAS)
VARIABLES_ERA5 = [
    "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "apparent_temperature_max",
    "relative_humidity_2m_mean", "dew_point_2m_mean", "precipitation_sum", "wind_speed_10m_max",
    "wind_gusts_10m_max", "et0_fao_evapotranspiration",
]


def clima_diario(lat: float | None = None, lon: float | None = None, inicio: str = "1950-01-01",
                 fin: str | None = None, variables: list[str] | None = None, forzar: bool = False) -> pd.DataFrame:
    """Serie diaria de ERA5 (Open-Meteo) en un punto; por defecto el centro de Leticia."""
    c = aoi_cfg()["centro"]
    lat, lon = lat if lat is not None else c["lat"], lon if lon is not None else c["lon"]
    fin = fin or (pd.Timestamp.today() - pd.Timedelta(days=7)).strftime("%Y-%m-%d")
    variables = variables or VARIABLES_ERA5

    def _bajar():
        partes = []
        anios = range(int(inicio[:4]), int(fin[:4]) + 1, 25)
        for a0 in anios:
            ini = max(pd.Timestamp(inicio), pd.Timestamp(f"{a0}-01-01"))
            fn = min(pd.Timestamp(fin), pd.Timestamp(f"{a0 + 24}-12-31"))
            r = _get(url("clima_diario"), params={
                "latitude": lat, "longitude": lon, "start_date": ini.strftime("%Y-%m-%d"), "end_date": fn.strftime("%Y-%m-%d"),
                "daily": ",".join(variables), "models": "era5", "timezone": "America/Bogota"})
            d = r.json()["daily"]
            partes.append(pd.DataFrame(d).set_index("time"))
            time.sleep(1)
        df = pd.concat(partes)
        df.index = pd.to_datetime(df.index)
        return df[~df.index.duplicated()]

    return cache(f"era5_{lat:.3f}_{lon:.3f}_{inicio[:4]}.csv", _bajar, forzar)


def caudal_glofas(lat: float | None = None, lon: float | None = None, inicio: str = "1984-01-01",
                  forzar: bool = False) -> pd.Series:
    """Caudal diario simulado por GloFAS v4 en la celda del Amazonas aguas arriba de Leticia."""
    p = aoi_cfg()["punto_glofas"]
    lat, lon = lat if lat is not None else p["lat"], lon if lon is not None else p["lon"]

    def _bajar():
        fin = (pd.Timestamp.today() - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
        r = _get(url("caudal_glofas"), params={"latitude": lat, "longitude": lon, "daily": "river_discharge",
                                               "start_date": inicio, "end_date": fin})
        d = r.json()
        s = pd.Series(d["daily"]["river_discharge"], index=pd.to_datetime(d["daily"]["time"]), name="caudal_m3s", dtype=float)
        return s.to_frame()

    df = cache(f"glofas_{lat:.2f}_{lon:.2f}.csv", _bajar, forzar)
    return df.iloc[:, 0] if isinstance(df, pd.DataFrame) else df


def pronostico_glofas(lat: float | None = None, lon: float | None = None, dias: int = 92) -> pd.DataFrame:
    """Pronóstico por ensamble de GloFAS (mediana, p25, p75, mín y máx) para los próximos meses. No se guarda en caché."""
    p = aoi_cfg()["punto_glofas"]
    lat, lon = lat if lat is not None else p["lat"], lon if lon is not None else p["lon"]
    var = "river_discharge_median,river_discharge_p25,river_discharge_p75,river_discharge_min,river_discharge_max"
    r = _get(url("caudal_glofas"), params={"latitude": lat, "longitude": lon, "daily": var, "forecast_days": dias,
                                           "past_days": 31, "ensemble": "true"})
    d = r.json()["daily"]
    return pd.DataFrame(d).set_index("time").rename(index=pd.Timestamp)


# ------------------------------------------------------------------ índices oceánicos (ENSO y Atlántico Norte)
def oni() -> pd.Series:
    """Índice Oceánico El Niño (ONI, NOAA CPC): anomalía trimestral móvil de la TSM en Niño 3.4."""

    def _bajar():
        txt = _get(url("indices_oceanicos")).text.split("\n")[1:]
        meses = {"DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "MJJ": 6, "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12}
        filas = [linea.split() for linea in txt if linea.strip()]
        idx = [pd.Timestamp(int(f[1]), meses[f[0]], 1) for f in filas]
        return pd.Series([float(f[3]) for f in filas], index=idx, name="valor").to_frame()

    df = cache("oni.csv", _bajar)
    return df.iloc[:, 0] if isinstance(df, pd.DataFrame) else df


# ------------------------------------------------------------------ CCKP (Banco Mundial)
def _cckp_url(variable: str, escenario: str, producto: str, periodo: str, percentil: str, agregacion: str = "annual") -> str:
    base = url("proyecciones_cckp")
    if producto == "timeseries":
        tipo, prod = "timeseries", "timeseries-smooth"
    else:
        tipo, prod = producto, "climatology"
    return (f"{base}/{variable}/ensemble-all-{escenario}/{tipo}-{variable}-{agregacion}-mean_cmip6-x0.25_"
            f"ensemble-all-{escenario}_{prod}_{percentil}_{periodo}.nc")


def _cckp_leer(u: str, lat: float, lon: float) -> tuple[np.ndarray, np.ndarray | None]:
    """Lee la celda más cercana de un NetCDF remoto con peticiones por rangos (no descarga el archivo global)."""
    import netCDF4

    for i in range(4):
        try:
            with netCDF4.Dataset(u + "#mode=bytes") as nc:
                la, lo = nc["lat"][:], nc["lon"][:]
                ii, jj = int(np.abs(la - lat).argmin()), int(np.abs(lo - lon).argmin())
                nombre = [k for k, v in nc.variables.items() if v.ndim == 3][0]
                valores = np.asarray(nc[nombre][:, ii, jj], dtype=float)
                t = None
                if "time" in nc.variables:
                    t = netCDF4.num2date(nc["time"][:], nc["time"].units, only_use_cftime_datetimes=False)
                    t = np.array([x.year for x in t])
                return valores, t
        except OSError as e:
            if i == 3:
                raise
            log.info("CCKP: reintento %s (%s)", u, e)
            time.sleep(5 * (i + 1))
    raise RuntimeError("inalcanzable")


def cckp_tabla(variables: list[str], escenarios: list[str] | None = None, periodos: list[str] | None = None,
               percentiles: list[str] | None = None, producto: str = "anomaly", forzar: bool = False) -> pd.DataFrame:
    """Cambio proyectado (o climatología) del ensamble CMIP6 del CCKP en la celda de Leticia.

    Devuelve una tabla larga: variable, escenario, periodo, percentil, valor. Las anomalías son
    respecto a 1995–2014 (definición del CCKP).
    """
    clima = aoi_cfg()["clima"]
    escenarios, periodos = escenarios or clima["escenarios"], periodos or clima["periodos_futuros"]
    percentiles = percentiles or clima["percentiles"]
    c = aoi_cfg()["centro"]
    p = ruta(f"cckp_{producto}.csv")
    previo = pd.read_csv(p) if p.exists() and not forzar else pd.DataFrame(columns=["variable", "escenario", "periodo", "percentil", "valor"])
    filas = []
    for v in variables:
        for e in escenarios:
            for per in periodos:
                for q in percentiles:
                    ya = previo[(previo.variable == v) & (previo.escenario == e) & (previo.periodo == per) & (previo.percentil == q)]
                    if len(ya):
                        filas.append(ya.iloc[0].to_dict())
                        continue
                    valores, _ = _cckp_leer(_cckp_url(v, e, producto, per, q), c["lat"], c["lon"])
                    filas.append({"variable": v, "escenario": e, "periodo": per, "percentil": q, "valor": float(valores[0])})
    nuevo = pd.DataFrame(filas)
    total = pd.concat([previo, nuevo]).drop_duplicates(["variable", "escenario", "periodo", "percentil"], keep="last")
    total.to_csv(p, index=False)
    return nuevo


def cckp_historico(variables: list[str], percentil: str = "median", forzar: bool = False) -> pd.Series:
    """Climatología 1995–2014 del ensamble (línea de base del CCKP) en la celda de Leticia."""
    c = aoi_cfg()["centro"]
    p = ruta("cckp_historico.csv")
    previo = pd.read_csv(p, index_col=0)["valor"] if p.exists() and not forzar else pd.Series(dtype=float, name="valor")
    for v in variables:
        if v in previo.index:
            continue
        u = (f"{url('proyecciones_cckp')}/{v}/ensemble-all-historical/climatology-{v}-annual-mean_cmip6-x0.25_"
             f"ensemble-all-historical_climatology_{percentil}_1995-2014.nc")
        previo.loc[v] = float(_cckp_leer(u, c["lat"], c["lon"])[0][0])
    previo.to_frame("valor").to_csv(p)
    return previo[variables]


def cckp_trayectoria(variable: str, escenarios: list[str] | None = None, percentiles: list[str] | None = None,
                     forzar: bool = False) -> pd.DataFrame:
    """Trayectoria anual suavizada 2015–2100 (ensamble CMIP6) por escenario y percentil."""
    escenarios = escenarios or aoi_cfg()["clima"]["escenarios"]
    percentiles = percentiles or ["p10", "median", "p90"]
    c = aoi_cfg()["centro"]

    def _bajar():
        cols = {}
        for e in escenarios:
            for q in percentiles:
                try:
                    v, anios = _cckp_leer(_cckp_url(variable, e, "timeseries", "2015-2100", q), c["lat"], c["lon"])
                    cols[f"{e}_{q}"] = pd.Series(v, index=anios)
                except OSError as err:  # el CCKP no publica todas las combinaciones
                    log.warning("CCKP sin %s %s %s: %s", variable, e, q, err)
        return pd.DataFrame(cols)

    df = cache(f"cckp_trayectoria_{variable}.csv", _bajar, forzar)
    for e in escenarios:
        for q in percentiles:
            if f"{e}_{q}" not in df:
                df[f"{e}_{q}"] = np.nan
    df.index = [int(pd.Timestamp(i).year) if not isinstance(i, (int, np.integer)) else int(i) for i in df.index]
    return df


# ------------------------------------------------------------------ límites, población y edificaciones
def limite_municipal(forzar: bool = False) -> gpd.GeoDataFrame:
    """Polígono del municipio (DANE vía geoBoundaries, versión simplificada)."""
    nombre = aoi_cfg()["municipio"]

    def _bajar():
        meta = _get(url("limite_municipal")).json()
        destino = dir_datos() / "raw" / "geoboundaries_COL_ADM2_simplificado.geojson"
        descargar(_github_crudo(meta["simplifiedGeometryGeoJSON"]), destino)
        g = gpd.read_file(destino)
        g = g[g["shapeName"].str.casefold() == nombre.casefold()].copy()
        return g[["shapeName", "shapeID", "geometry"]].to_crs(4326)

    return cache(f"limite_{aoi_cfg()['slug']}.parquet", _bajar, forzar)


def _quadkey(lon: float, lat: float, z: int) -> str:
    x = (lon + 180) / 360
    s = math.sin(math.radians(lat))
    y = 0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)
    n = 2 ** z
    tx, ty = int(x * n), int(y * n)
    q = ""
    for i in range(z, 0, -1):
        d, m = 0, 1 << (i - 1)
        d += 1 if tx & m else 0
        d += 2 if ty & m else 0
        q += str(d)
    return q


def edificaciones(clave_bbox: str = "bbox_urbano", forzar: bool = False) -> gpd.GeoDataFrame:
    """Huellas de edificaciones de Microsoft (Global ML Building Footprints) dentro de la extensión."""
    b = bbox(clave_bbox)

    def _bajar():
        enlaces = pd.read_csv(io.StringIO(_get(url("edificaciones")).text))
        claves = {_quadkey(x, y, 9) for x in (b[0], b[2]) for y in (b[1], b[3])}
        filas = enlaces[enlaces["QuadKey"].astype(str).str.zfill(9).isin(claves) & (enlaces["Location"] == "Colombia")]
        geoms, alturas = [], []
        for u in filas["Url"]:
            contenido = gzip.decompress(_get(u).content).decode()
            for linea in contenido.splitlines():
                if not linea.strip():
                    continue
                f = json.loads(linea)
                g = shape(f["geometry"])
                if g.intersects(box(*b)):
                    geoms.append(g)
                    alturas.append(f.get("properties", {}).get("height", -1))
        gdf = gpd.GeoDataFrame({"altura_m": alturas}, geometry=geoms, crs=4326)
        gdf["altura_m"] = pd.to_numeric(gdf["altura_m"], errors="coerce").where(lambda s: s > 0)
        return gdf

    return cache(f"edificaciones_{clave_bbox}.parquet", _bajar, forzar)


def poblacion(clave_bbox: str = "bbox_urbano", forzar: bool = False) -> gpd.GeoDataFrame:
    """Población de Kontur en hexágonos H3 (r8) que tocan la extensión."""
    b = bbox(clave_bbox, 0.01)

    def _bajar():
        gz = descargar(url("poblacion"), dir_datos() / "raw" / Path(url("poblacion")).name)
        gpkg = gz.with_suffix("")
        if not gpkg.exists():
            with gzip.open(gz) as fi, open(gpkg, "wb") as fo:
                shutil.copyfileobj(fi, fo)
        g = gpd.read_file(gpkg, bbox=tuple(gpd.GeoSeries([box(*b)], crs=4326).to_crs(3857).total_bounds))
        return g.to_crs(4326)[["h3", "population", "geometry"]]

    return cache(f"poblacion_{clave_bbox}.parquet", _bajar, forzar)


def lugares_clave(consultas: dict[str, str] | None = None, forzar: bool = False) -> gpd.GeoDataFrame:
    """Geocodifica infraestructura crítica con Nominatim (una consulta por segundo)."""
    consultas = consultas or {
        "Hospital San Rafael": "Hospital San Rafael, Leticia, Amazonas, Colombia",
        "Aeropuerto Vásquez Cobo": "Aeropuerto Internacional Alfredo Vásquez Cobo, Leticia",
        "Muelle de Leticia": "Muelle, Leticia, Amazonas, Colombia",
        "Malecón": "Malecón, Leticia, Amazonas, Colombia",
        "Parque Santander": "Parque Santander, Leticia, Amazonas, Colombia",
        "Universidad Nacional (sede Amazonia)": "Universidad Nacional de Colombia Sede Amazonia, Leticia",
    }

    def _bajar():
        filas = []
        for nombre, q in consultas.items():
            r = _get(url("lugares_clave"), params={"q": q, "format": "json", "limit": 1, "countrycodes": "co"})
            res = r.json()
            if res:
                filas.append({"nombre": nombre, "lon": float(res[0]["lon"]), "lat": float(res[0]["lat"]), "osm": res[0].get("display_name", "")[:90]})
            time.sleep(1.1)
        df = pd.DataFrame(filas)
        return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs=4326)

    return cache("lugares_clave.parquet", _bajar, forzar)


# ------------------------------------------------------------------ rásteres remotos
def _leer_ventana(urls: list[str], b: tuple, nodata=None):
    """Lee la ventana `b` de una o varias teselas COG/GeoTIFF remotas y las une en un DataArray."""
    import rioxarray  # noqa: F401
    import xarray as xr
    from rioxarray.merge import merge_arrays

    partes = []
    for u in urls:
        da = xr.open_dataarray("/vsicurl/" + u, engine="rasterio").squeeze(drop=True)
        x0, x1 = float(da.x.min()), float(da.x.max())
        y0, y1 = float(da.y.min()), float(da.y.max())
        if b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1:
            continue
        partes.append(da.rio.clip_box(*b).load())
    if not partes:
        raise LookupError("Ninguna tesela cubre la extensión pedida")
    out = partes[0] if len(partes) == 1 else merge_arrays(partes)
    if nodata is not None:
        out = out.where(out != nodata)
    return out


def _teselas_10grados(b: tuple) -> list[str]:
    """Nombres de teselas de 10° tipo Hansen/GFC (esquina superior izquierda), p. ej. 00N_070W."""
    nombres = []
    for lon0 in range(int(math.floor(b[0] / 10) * 10), int(math.floor(b[2] / 10) * 10) + 1, 10):
        for lat_sup in range(int(math.ceil(b[1] / 10) * 10), int(math.ceil(b[3] / 10) * 10) + 1, 10):
            ns = f"{abs(lat_sup):02d}{'N' if lat_sup >= 0 else 'S'}"
            ew = f"{abs(lon0):03d}{'E' if lon0 >= 0 else 'W'}"
            nombres.append(f"{ns}_{ew}")
    return sorted(set(nombres))


def bosque_hansen(capa: str = "lossyear", clave_bbox: str = "bbox_regional", forzar: bool = False):
    """Global Forest Change (Hansen et al.): `lossyear` (año de pérdida 1–24) o `treecover2000` (%)."""
    b = bbox(clave_bbox)
    version = url("perdida_bosque").rstrip("/").split("/")[-1]

    def _bajar():
        urls = [f"{url('perdida_bosque')}/Hansen_{version}_{capa}_{t}.tif" for t in _teselas_10grados(b)]
        return _leer_ventana(urls, b)

    return cache(f"hansen_{capa}_{clave_bbox}.tif", _bajar, forzar)


def inundacion_jrc(periodo_retorno: int = 100, clave_bbox: str = "bbox_regional", forzar: bool = False):
    """Profundidad de inundación fluvial (m) del JRC/GloFAS para un periodo de retorno."""
    b = bbox(clave_bbox)

    def _bajar():
        base = url("inundacion_jrc")
        teselas = gpd.read_file(io.BytesIO(_get(f"{base}/tile_extents.geojson").content))
        sel = teselas[teselas.intersects(box(*b))]
        urls = [f"{base}/RP{periodo_retorno}/ID{i}_{n}_RP{periodo_retorno}_depth.tif" for i, n in zip(sel["id"], sel["name"])]
        return _leer_ventana(urls, b, nodata=-9999)

    return cache(f"jrc_inundacion_rp{periodo_retorno}_{clave_bbox}.tif", _bajar, forzar)


# ------------------------------------------------------------------ Planetary Computer (STAC)
def catalogo_pc():
    import planetary_computer
    import pystac_client

    return pystac_client.Client.open(url("landsat"), modifier=planetary_computer.sign_inplace)


def raster_estatico(coleccion: str, activo: str, clave_bbox: str = "bbox_regional", resolucion: float | None = None,
                    nombre: str | None = None, forzar: bool = False):
    """Capa estática de Planetary Computer (DEM, JRC GSW, WorldCover) recortada a la extensión, en EPSG:4326."""
    b = bbox(clave_bbox)
    nombre = nombre or f"{coleccion}_{activo}_{clave_bbox}.tif"

    def _bajar():
        import odc.stac

        items = list(catalogo_pc().search(collections=[coleccion], bbox=b).items())
        if coleccion == "esa-worldcover":
            items = [i for i in items if "2021" in i.id] or items
        if coleccion == "jrc-gsw":
            ultimo = max(i.id.split("v")[-1] for i in items)
            items = [i for i in items if i.id.endswith(ultimo)]
        ds = odc.stac.load(items, bands=[activo], bbox=b, crs="EPSG:4326",
                           resolution=resolucion or 0.000277777777778, groupby="solar_day" if coleccion != "jrc-gsw" else "id")
        da = ds[activo].max("time") if "time" in ds.dims else ds[activo]
        ren = {k: v for k, v in (("latitude", "y"), ("longitude", "x")) if k in da.dims}
        return da.rename(ren).rio.write_crs(4326)

    return cache(nombre, _bajar, forzar)


# ------------------------------------------------------------------ FIRMS
def focos_calor(sensor: str = "modis", anios: list[int] | None = None, clave_bbox: str = "bbox_regional",
                pais: str = "Colombia") -> pd.DataFrame:
    """Focos de calor del archivo anual por país de NASA FIRMS, recortados a la extensión.

    sensor: "modis" (2001–) o "viirs-snpp" (2012–). Cada año se guarda por separado.
    """
    b = bbox(clave_bbox)
    anios = anios or list(range(2001 if sensor == "modis" else 2012, date.today().year))
    partes = []
    for a in anios:
        def _bajar(a=a):
            u = f"{url('focos_calor')}/{sensor}/{a}/{sensor}_{a}_{pais}.csv"
            df = pd.read_csv(io.StringIO(_get(u).text))
            df = df[df.longitude.between(b[0], b[2]) & df.latitude.between(b[1], b[3])]
            return df.set_index(pd.to_datetime(df["acq_date"]))

        try:
            partes.append(cache(f"firms_{sensor}_{a}_{clave_bbox}.csv", _bajar))
        except requests.HTTPError as e:
            log.warning("FIRMS %s %s no disponible: %s", sensor, a, e)
    return pd.concat(partes).sort_index() if partes else pd.DataFrame()
