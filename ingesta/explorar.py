import os
import sys
import time
import requests

BASE = "https://www.datos.gov.co"
SECOP = "jbjy-vk9h"
TVEC = "rgxm-mmea"

FECHA_SECOP = "fecha_de_firma"
ANIOS = range(2020, 2027)
ANIO_MUESTRA = 2025

TERMINOS = {
    "microsoft": ["MICROSOFT", "AZURE", "OFFICE 365", "MICROSOFT 365"],
    "oracle": ["ORACLE"],
    "aws": ["AMAZON WEB SERVICES", " AWS "],
    "google": ["GOOGLE CLOUD", "GOOGLE WORKSPACE", "G SUITE"],
}

sesion = requests.Session()
token = os.environ.get("SOCRATA_APP_TOKEN")
if token:
    sesion.headers["X-App-Token"] = token


def columnas(dataset):
    r = sesion.get(f"{BASE}/api/views/{dataset}.json", timeout=60)
    r.raise_for_status()
    return sorted(c["fieldName"] for c in r.json()["columns"])


REINTENTAR = {429, 500, 502, 503, 504}


def soql(dataset, **params):
    params = {f"${k}": v for k, v in params.items()}
    for intento in range(5):
        if intento:
            time.sleep(15 * intento)
        try:
            r = sesion.get(f"{BASE}/resource/{dataset}.json", params=params, timeout=300)
        except requests.Timeout:
            if intento == 4:
                raise
            continue
        if r.status_code not in REINTENTAR or intento == 4:
            r.raise_for_status()
            return r.json()


def entre(campo, anio):
    return f"{campo} between '{anio}-01-01T00:00:00' and '{anio}-12-31T23:59:59'"


def condicion_texto(terminos, campo="objeto_del_contrato"):
    return " OR ".join(f"upper({campo}) like '%{t}%'" for t in terminos)


def consultar(titulo, dataset, **params):
    print(f"-> {titulo}", file=sys.stderr, flush=True)
    try:
        filas = soql(dataset, **params)
    except requests.RequestException as e:
        filas = [f"falló: {e}"]
    print(f"\n== {titulo} ==")
    for fila in filas:
        print(fila)


if __name__ == "__main__":
    print("== Columnas de fecha en SECOP II ==")
    for c in columnas(SECOP):
        if "fecha" in c:
            print(c)

    for anio in ANIOS:
        consultar(f"SECOP II: contratos firmados en {anio}", SECOP,
                  select="count(*) as n", where=entre(FECHA_SECOP, anio))

    muestra = entre(FECHA_SECOP, ANIO_MUESTRA)

    consultar(f"Estados de contrato ({ANIO_MUESTRA})", SECOP,
              select="estado_contrato, count(*) as n", where=muestra,
              group="estado_contrato", order="n desc")

    for fabricante, terminos in TERMINOS.items():
        filtro = f"{muestra} AND ({condicion_texto(terminos)})"
        consultar(f"{fabricante} ({ANIO_MUESTRA}): total y valor", SECOP,
                  select="count(*) as n, sum(valor_del_contrato) as valor",
                  where=filtro)
        consultar(f"{fabricante} ({ANIO_MUESTRA}): códigos UNSPSC más frecuentes", SECOP,
                  select="codigo_de_categoria_principal, count(*) as n",
                  where=filtro, group="codigo_de_categoria_principal",
                  order="n desc", limit=15)

    consultar("TVEC: acuerdos marco con más valor desde 2020", TVEC,
              select="agregacion, count(*) as n, sum(total) as valor",
              where="fecha >= '2020-01-01T00:00:00'", group="agregacion",
              order="valor desc", limit=40)