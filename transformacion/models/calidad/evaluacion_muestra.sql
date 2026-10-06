select
    e.fuente,
    e.id,
    e.tipo_gasto_real,
    c.tipo_gasto,
    c.regla_aplicada,
    e.fabricante_real,
    c.fabricante,
    e.tipo_gasto_real = c.tipo_gasto as acierta_tipo,
    e.fabricante_real = c.fabricante as acierta_fabricante,
    e.tipo_gasto_real <> 'fuera_de_alcance' as en_alcance,
    e.nota,
    c.texto
from {{ ref('etiquetas_manuales') }} e
left join {{ ref('int_clasificacion') }} c
    on c.fuente = e.fuente and c.id = e.id