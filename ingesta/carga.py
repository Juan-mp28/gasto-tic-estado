from dataclasses import dataclass
from typing import Callable

from api import soql, paginar
from db import conectar


@dataclass
class Fuente:
    nombre: str
    dataset: str
    tabla: str
    llave: str
    columnas_api: list[str]
    columnas_destino: list[str]
    filtro: Callable[[str, str], str]
    a_fila: Callable[[dict], list]

    def upsert(self):
        cols = self.columnas_destino
        return (
            f"insert into {self.tabla} ({', '.join(cols)}) "
            f"values ({', '.join(['%s'] * len(cols))}) "
            f"on conflict ({self.llave}) do update set "
            + ", ".join(f"{c} = excluded.{c}" for c in cols if c != self.llave)
            + ", cargado_en = now()"
        )


def meses(desde, hasta):
    anio, mes = map(int, desde.split("-"))
    fin = tuple(map(int, hasta.split("-")))
    while (anio, mes) <= fin:
        sig_anio, sig_mes = anio + mes // 12, mes % 12 + 1
        yield f"{anio}-{mes:02d}-01", f"{sig_anio}-{sig_mes:02d}-01"
        anio, mes = sig_anio, sig_mes


def cargar_mes(conn, fuente, desde, hasta):
    where = fuente.filtro(desde, hasta)
    esperadas = int(soql(fuente.dataset, select="count(*) as n", where=where)[0]["n"])
    filas = [fuente.a_fila(r)
             for r in paginar(fuente.dataset, where, fuente.llave, fuente.columnas_api)]
    conn.cursor().executemany(fuente.upsert(), filas)

    pos = fuente.columnas_destino.index(fuente.llave)
    unicas = len({f[pos] for f in filas})
    return esperadas, len(filas), unicas


def registrar(conn, carga, estado, detalle, filas=None):
    conn.execute(
        "update raw.cargas set estado = %s, filas = %s, detalle = %s, terminada_en = now() "
        "where id = %s",
        [estado, filas, detalle, carga],
    )
    conn.commit()


def ejecutar(fuente, desde, hasta):
    con_problemas = []

    with conectar() as conn:
        for inicio, fin in meses(desde, hasta):
            mes = inicio[:7]
            carga = conn.execute(
                "insert into raw.cargas (fuente, detalle) values (%s, %s) returning id",
                [fuente.nombre, mes],
            ).fetchone()[0]
            conn.commit()

            try:
                esperadas, leidas, unicas = cargar_mes(conn, fuente, inicio, fin)
            except Exception as e:
                conn.rollback()
                registrar(conn, carga, "error", f"{mes}: {e}")
                print(f"{fuente.nombre} {mes}  ERROR  {e}")
                con_problemas.append(mes)
                continue

            estado = "ok" if leidas == esperadas else "incompleta"
            detalle = f"{mes}: esperadas={esperadas} leidas={leidas} unicas={unicas}"
            registrar(conn, carga, estado, detalle, unicas)
            print(f"{fuente.nombre} {detalle}  {estado}")
            if estado != "ok":
                con_problemas.append(mes)

    return con_problemas