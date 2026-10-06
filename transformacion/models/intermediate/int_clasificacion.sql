with registros as (
    select * from {{ ref('int_registros') }}
),

por_texto as (
    select r.fuente, r.id, t.fabricante
    from registros r
    join {{ ref('terminos_fabricante') }} t on r.texto_normalizado ~ t.patron
),

por_proveedor as (
    select r.fuente, r.id, p.fabricante
    from registros r
    join {{ ref('proveedores_fabricante') }} p on {{ normalizar('r.proveedor') }} ~ p.patron
),

fabricantes as (
    select fuente, id, array_agg(distinct fabricante order by fabricante) as detectados
    from (
        select * from por_texto
        union
        select * from por_proveedor
    ) coincidencias
    group by fuente, id
),

tipo as (
    select distinct on (r.fuente, r.id)
        r.fuente, r.id, g.tipo_gasto, g.regla
    from registros r
    join {{ ref('reglas_tipo_gasto') }} g on r.texto_normalizado ~ g.patron
    order by r.fuente, r.id, g.prioridad
)

select
    r.*,
    case
        when cardinality(f.detectados) = 1 then f.detectados[1]
        when cardinality(f.detectados) > 1 then 'multi_fabricante'
        else 'otros'
    end as fabricante,
    f.detectados as fabricantes_detectados,
    coalesce(t.tipo_gasto, 'sin_clasificar') as tipo_gasto,
    t.regla as regla_aplicada
from registros r
left join fabricantes f using (fuente, id)
left join tipo t using (fuente, id)
