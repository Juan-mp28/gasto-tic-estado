{{ config(severity='warn') }}

select fuente, id, nombre_entidad, valor
from {{ ref('fct_gasto_tic') }}
where valor > 1e12