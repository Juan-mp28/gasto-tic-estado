with origen as (
    select * from {{ source('raw', 'secop_contratos') }}
)

select
    id_contrato,
    proceso_de_compra,
    nombre_entidad,
    nit_entidad,
    codigo_entidad,
    departamento,
    ciudad,
    orden as orden_entidad,
    sector,
    rama,
    estado_contrato,
    nullif(replace(codigo_de_categoria_principal, 'V1.', ''), 'UNSPECIFIED') as codigo_unspsc,
    objeto_del_contrato,
    {{ normalizar('objeto_del_contrato') }} as objeto_normalizado,
    tipo_de_contrato,
    modalidad_de_contratacion,
    {{ a_fecha('fecha_de_firma') }} as fecha_firma,
    {{ a_fecha('fecha_de_inicio_del_contrato') }} as fecha_inicio,
    {{ a_fecha('fecha_de_fin_del_contrato') }} as fecha_fin,
    proveedor_adjudicado,
    documento_proveedor,
    {{ a_numero('valor_del_contrato') }} as valor,
    url_proceso,
    cargado_en
from origen