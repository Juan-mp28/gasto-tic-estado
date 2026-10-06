with secop as (
    select
        'secop' as fuente,
        id_contrato as id,
        nombre_entidad,
        nit_entidad,
        proveedor_adjudicado as proveedor,
        fecha_firma as fecha,
        valor,
        estado_contrato as estado,
        estado_contrato in ('Borrador', 'Cancelado') as excluido_por_estado,
        codigo_unspsc,
        objeto_del_contrato as texto,
        objeto_normalizado as texto_normalizado,
        url_proceso
    from {{ ref('stg_secop_contratos') }}
),

tvec as (
    select
        'tvec',
        id_orden,
        nombre_entidad,
        nit_entidad,
        proveedor,
        fecha_orden,
        valor,
        estado,
        estado = 'Cancelado',
        null,
        concat_ws(' | ', agregacion, items),
        concat_ws(' | ', agregacion_normalizada, items_normalizados),
        null
    from {{ ref('stg_tvec_ordenes') }}
)

select * from secop
union all
select * from tvec