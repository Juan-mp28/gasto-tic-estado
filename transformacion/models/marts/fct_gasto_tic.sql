select
    fuente,
    id,
    nombre_entidad,
    nit_entidad,
    proveedor,
    fecha,
    extract(year from fecha)::int as anio,
    fabricante,
    tipo_gasto,
    valor,
    regla_aplicada,
    texto,
    url_proceso
from {{ ref('int_clasificacion') }}
where tipo_gasto in ('nube', 'licencia')
  and not excluido_por_estado
