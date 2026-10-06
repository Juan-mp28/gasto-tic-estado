import sys

from api import soql, paginar, contiene, empieza
from db import conectar

DATASET = "jbjy-vk9h"

FABRICANTES = ["MICROSOFT", "AZURE", "OFFICE 365", "ORACLE", "AMAZON WEB SERVICES",
               "AWS", "GOOGLE", "GCP", "UNIFIED"]
DIRECTAS = ["NUBE", "CLOUD", "SOFTWARE"]
CONDICIONADAS = ["LICENCI", "SUSCRIPCI"]
UNSPSC_TIC = ["V1.43", "V1.8111", "V1.8116"]

COLUMNAS = [
    "id_contrato", "proceso_de_compra", "nombre_entidad", "nit_entidad", "codigo_entidad",
    "departamento", "ciudad", "orden", "sector", "rama", "estado_contrato",
    "codigo_de_categoria_principal", "objeto_del_contrato", "descripcion_del_proceso",
    "tipo_de_contrato", "modalidad_de_contratacion", "fecha_de_firma",
    "fecha_de_inicio_del_contrato", "fecha_de_fin_del_contrato", "proveedor_adjudicado",
    "documento_proveedor", "valor_del_contrato",
]
DESTINO = COLUMNAS + ["url_proceso"]

UPSERT = (
    f"insert into raw.secop_contratos ({', '.join(DESTINO)}) "
    f"values ({', '.join(['%s'] * len(DESTINO))}) "
    f"on conflict (id_contrato) do update set "
    + ", ".join(f"{c} = excluded.{c}" for c in DESTINO[1:])
    + ", cargado_en = now()"
)


def filtro(desde, hasta):
    objeto = "objeto_del_contrato"
    tic = empieza("codigo_de_categoria_principal", UNSPSC_TIC)
    return (
        f"fecha_de_firma >= '{desde}T00:00:00' AND fecha_de_firma < '{hasta}T00:00:00' "
        f"AND ({contiene(objeto, FABRICANTES + DIRECTAS)} "
        f"OR (({contiene(objeto, CONDICIONADAS)}) AND ({tic})))"
    )


def meses(desde, hasta):
    anio, mes = map(int, desde.split("-"))
    fin = tuple(map(int, hasta.split("-")))
    while (anio, mes) <= fin:
        sig_anio, sig_mes = anio + mes // 12, mes % 12 + 1
        yield f"{anio}-{mes:02d}-01", f"{sig_anio}-{sig_mes:02d}-01"
        anio, mes = sig_anio, sig_mes


def a_fila(registro):
    url = (registro.get("urlproceso") or {}).get("url")
    return [registro.get(c) for c in COLUMNAS] + [url]


def cargar_mes(conn, desde, hasta):
    where = filtro(desde, hasta)
    esperadas = int(soql(DATASET, select="count(*) as n", where=where)[0]["n"])
    filas = [a_fila(r) for r in paginar(DATASET, where, "id_contrato", COLUMNAS + ["urlproceso"])]
    conn.cursor().executemany(UPSERT, filas)
    unicas = len({f[0] for f in filas})
    return esperadas, len(filas), unicas


def registrar(conn, carga, estado, detalle, filas=None):
    conn.execute(
        "update raw.cargas set estado = %s, filas = %s, detalle = %s, terminada_en = now() "
        "where id = %s",
        [estado, filas, detalle, carga],
    )
    conn.commit()


if __name__ == "__main__":
    desde, hasta = sys.argv[1], sys.argv[2]

    with conectar() as conn:
        for inicio, fin in meses(desde, hasta):
            mes = inicio[:7]
            carga = conn.execute(
                "insert into raw.cargas (fuente, detalle) values ('secop', %s) returning id", [mes]
            ).fetchone()[0]
            conn.commit()

            try:
                esperadas, leidas, unicas = cargar_mes(conn, inicio, fin)
            except Exception as e:
                conn.rollback()
                registrar(conn, carga, "error", f"{mes}: {e}")
                print(f"{mes}  ERROR  {e}")
                continue

            estado = "ok" if leidas == esperadas else "incompleta"
            detalle = f"{mes}: esperadas={esperadas} leidas={leidas} unicas={unicas}"
            registrar(conn, carga, estado, detalle, unicas)
            print(f"{detalle}  {estado}")