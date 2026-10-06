select
    {{ normalizar('nombre_entidad') }} as entidad,
    fabricante,
    anio,
    count(*) as contratos,
    sum(valor) as valor_total,
    coalesce(sum(valor) filter (where tipo_gasto = 'nube'), 0) as valor_nube,
    coalesce(sum(valor) filter (where tipo_gasto = 'licencia'), 0) as valor_licencia
from {{ ref('fct_gasto_tic') }}
group by 1, 2, 3