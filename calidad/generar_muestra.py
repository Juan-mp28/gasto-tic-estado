import csv

import psycopg

CONSULTA = """
with base as (
    select 'secop' as fuente, id_contrato as id, nombre_entidad,
           proveedor_adjudicado as proveedor, valor,
           objeto_del_contrato as texto, url_proceso as url
    from analitica.stg_secop_contratos
    where estado_contrato not in ('Borrador', 'Cancelado')

    union all

    select 'tvec', id_orden, nombre_entidad, proveedor, valor,
           coalesce(agregacion, 'Sin agregación') || ' | ' || left(items, 600), null
    from analitica.stg_tvec_ordenes
    where estado <> 'Cancelado'
),
mayores as (
    select *, 'mayor_valor' as estrato from base
    order by valor desc limit 30
),
azar as (
    select *, 'azar' as estrato from base
    where id not in (select id from mayores)
    order by md5(id) limit 30
)
select * from mayores
union all
select * from azar
"""

COLUMNAS = ["estrato", "fuente", "id", "nombre_entidad", "proveedor", "valor", "texto", "url",
            "fabricante_real", "tipo_gasto_real", "nota"]

if __name__ == "__main__":
    with psycopg.connect() as conn:
        filas = conn.execute(CONSULTA).fetchall()

    with open("calidad/muestra_para_etiquetar.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(COLUMNAS)
        for fuente, id_, entidad, proveedor, valor, texto, url, estrato in filas:
            escritor.writerow([estrato, fuente, id_, entidad, proveedor, valor, texto, url, "", "", ""])

    print(f"{len(filas)} registros en calidad/muestra_para_etiquetar.csv")