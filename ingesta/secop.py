import sys

from api import contiene, empieza
from carga import Fuente, ejecutar
from reglas import FABRICANTES, DIRECTAS, CONDICIONADAS, UNSPSC_TIC

COLUMNAS = [
    "id_contrato", "proceso_de_compra", "nombre_entidad", "nit_entidad", "codigo_entidad",
    "departamento", "ciudad", "orden", "sector", "rama", "estado_contrato",
    "codigo_de_categoria_principal", "objeto_del_contrato", "descripcion_del_proceso",
    "tipo_de_contrato", "modalidad_de_contratacion", "fecha_de_firma",
    "fecha_de_inicio_del_contrato", "fecha_de_fin_del_contrato", "proveedor_adjudicado",
    "documento_proveedor", "valor_del_contrato",
]


def filtro(desde, hasta):
    objeto = "objeto_del_contrato"
    tic = empieza("codigo_de_categoria_principal", UNSPSC_TIC)
    return (
        f"fecha_de_firma >= '{desde}T00:00:00' AND fecha_de_firma < '{hasta}T00:00:00' "
        f"AND ({contiene(objeto, FABRICANTES + DIRECTAS)} "
        f"OR (({contiene(objeto, CONDICIONADAS)}) AND ({tic})))"
    )


def a_fila(registro):
    url = (registro.get("urlproceso") or {}).get("url")
    return [registro.get(c) for c in COLUMNAS] + [url]


SECOP = Fuente(
    nombre="secop",
    dataset="jbjy-vk9h",
    tabla="raw.secop_contratos",
    llave="id_contrato",
    columnas_api=COLUMNAS + ["urlproceso"],
    columnas_destino=COLUMNAS + ["url_proceso"],
    filtro=filtro,
    a_fila=a_fila,
)

if __name__ == "__main__":
    ejecutar(SECOP, sys.argv[1], sys.argv[2])