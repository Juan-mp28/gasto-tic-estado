from explorar import SECOP, FECHA_SECOP, TERMINOS, consultar, entre, condicion_texto

ANIO = 2025
GENERICAS = ["LICENCI", "NUBE", "CLOUD", "SUSCRIPCI", "SOFTWARE"]
FAMILIAS_TIC = ["V1.4323", "V1.8111"]
CAMPOS = "id_contrato, codigo_de_categoria_principal, valor_del_contrato, objeto_del_contrato"

rango = entre(FECHA_SECOP, ANIO)
fabricantes = [t for lista in TERMINOS.values() for t in lista]
sin_fabricante = f"NOT ({condicion_texto(fabricantes)})"


if __name__ == "__main__":
    for palabra in GENERICAS:
        filtro = f"{rango} AND upper(objeto_del_contrato) like '%{palabra}%' AND {sin_fabricante}"

        consultar(f"{palabra}: total sin fabricante", SECOP,
                  select="count(*) as n, sum(valor_del_contrato) as valor", where=filtro)
        consultar(f"{palabra}: 10 de mayor valor", SECOP,
                  select=CAMPOS, where=filtro, order="valor_del_contrato desc", limit=10)
        consultar(f"{palabra}: 10 sin mirar valor", SECOP,
                  select=CAMPOS, where=filtro, order="id_contrato", limit=10)

    familias = " OR ".join(
        f"starts_with(codigo_de_categoria_principal, '{f}')" for f in FAMILIAS_TIC)
    sin_palabras = f"NOT ({condicion_texto(fabricantes + GENERICAS)})"
    filtro = f"{rango} AND ({familias}) AND {sin_palabras}"

    consultar("UNSPSC TIC sin ninguna palabra: total", SECOP,
              select="count(*) as n, sum(valor_del_contrato) as valor", where=filtro)
    consultar("UNSPSC TIC sin ninguna palabra: 15 de mayor valor", SECOP,
              select=CAMPOS, where=filtro, order="valor_del_contrato desc", limit=15)