import sys

from api import contiene
from carga import Fuente, ejecutar
from reglas import FABRICANTES, DIRECTAS

COLUMNAS = [
    "identificador_de_la_orden", "a_o", "fecha", "entidad", "nit_entidad", "id_entidad",
    "rama_de_la_entidad", "orden_de_la_entidad", "sector_de_la_entidad", "ciudad",
    "proveedor", "nit_proveedor", "estado", "solicitud", "agregacion", "items", "total",
]
TERMINOS = FABRICANTES + DIRECTAS


def filtro(desde, hasta):
    return (
        f"fecha >= '{desde}T00:00:00' AND fecha < '{hasta}T00:00:00' "
        f"AND (({contiene('agregacion', TERMINOS)}) OR ({contiene('items', TERMINOS)}))"
    )


def a_fila(registro):
    return [registro.get(c) for c in COLUMNAS]


TVEC = Fuente(
    nombre="tvec",
    dataset="rgxm-mmea",
    tabla="raw.tvec_ordenes",
    llave="identificador_de_la_orden",
    columnas_api=COLUMNAS,
    columnas_destino=COLUMNAS,
    filtro=filtro,
    a_fila=a_fila,
)

if __name__ == "__main__":
    ejecutar(TVEC, sys.argv[1], sys.argv[2])