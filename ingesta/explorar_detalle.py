from explorar import (SECOP, TVEC, FECHA_SECOP, ANIOS, ANIO_MUESTRA, TERMINOS,
                      consultar, entre, condicion_texto)

FAMILIAS_TIC = ["V1.4323", "V1.8111"]
PALABRAS_TVEC = ["SOFTWARE", "NUBE", "MICROSOFT", "ORACLE", "GOOGLE", "AMAZON"]


if __name__ == "__main__":
    for anio in ANIOS:
        rango = entre(FECHA_SECOP, anio)
        for familia in FAMILIAS_TIC:
            consultar(f"SECOP II {anio}: UNSPSC {familia}*", SECOP,
                      select="count(*) as n, sum(valor_del_contrato) as valor",
                      where=f"{rango} AND starts_with(codigo_de_categoria_principal, '{familia}')")

    muestra = entre(FECHA_SECOP, ANIO_MUESTRA)
    for fabricante in ["microsoft", "oracle"]:
        consultar(f"{fabricante} ({ANIO_MUESTRA}): contratos de mayor valor", SECOP,
                  select="codigo_de_categoria_principal, proveedor_adjudicado, "
                         "valor_del_contrato, objeto_del_contrato",
                  where=f"{muestra} AND ({condicion_texto(TERMINOS[fabricante])})",
                  order="valor_del_contrato desc", limit=20)

    consultar("TVEC: acuerdos de software, nube y fabricantes desde 2020", TVEC,
              select="agregacion, count(*) as n, sum(total) as valor",
              where=f"fecha >= '2020-01-01T00:00:00' AND "
                    f"({condicion_texto(PALABRAS_TVEC, campo='agregacion')})",
              group="agregacion", order="valor desc")

    for anio in ANIOS:
        consultar(f"TVEC {anio}: órdenes 'No Definido'", TVEC,
                  select="count(*) as n, sum(total) as valor",
                  where=f"agregacion = 'No Definido' AND {entre('fecha', anio)}")

    consultar("TVEC: 'No Definido' de mayor valor", TVEC,
              select="fecha, entidad, proveedor, items, total",
              where="agregacion = 'No Definido'", order="total desc", limit=30)