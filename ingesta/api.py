import os
import time

import requests

BASE = "https://www.datos.gov.co"
REINTENTAR = {429, 500, 502, 503, 504}

sesion = requests.Session()
if os.environ.get("SOCRATA_APP_TOKEN"):
    sesion.headers["X-App-Token"] = os.environ["SOCRATA_APP_TOKEN"]


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


def paginar(dataset, where, orden, columnas, tamano=1000):
    offset = 0
    while True:
        filas = soql(dataset, select=", ".join(columnas), where=where,
                     order=orden, limit=tamano, offset=offset)
        yield from filas
        if len(filas) < tamano:
            return
        offset += tamano


def contiene(campo, terminos):
    return " OR ".join(f"upper({campo}) like '%{t}%'" for t in terminos)


def empieza(campo, prefijos):
    return " OR ".join(f"starts_with({campo}, '{p}')" for p in prefijos)