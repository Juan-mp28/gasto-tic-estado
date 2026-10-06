select
    fuente,
    {{ normalizar('nombre_entidad') }} as entidad,
    count(*) as registros,
    count(*) filter (where excluido_por_estado) as excluidos,
    round(100.0 * count(*) filter (where excluido_por_estado) / count(*), 1) as pct_excluidos
from {{ ref('int_clasificacion') }}
where tipo_gasto in ('nube', 'licencia')
group by 1, 2