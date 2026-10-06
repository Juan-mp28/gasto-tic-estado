with origen as (
    select * from {{ source('raw', 'tvec_ordenes') }}
)

select
    identificador_de_la_orden as id_orden,
    solicitud,
    entidad as nombre_entidad,
    nit_entidad,
    id_entidad,
    rama_de_la_entidad,
    orden_de_la_entidad,
    sector_de_la_entidad,
    ciudad,
    proveedor,
    nit_proveedor,
    estado,
    nullif(agregacion, 'No Definido') as agregacion,
    {{ normalizar("nullif(agregacion, 'No Definido')") }} as agregacion_normalizada,
    items,
    {{ normalizar('items') }} as items_normalizados,
    {{ a_fecha('fecha') }} as fecha_orden,
    {{ a_numero('total') }} as valor,
    cargado_en
from origen