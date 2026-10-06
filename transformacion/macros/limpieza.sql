{% macro normalizar(columna) %}
    trim(regexp_replace(
        translate(upper(replace({{ columna }}, chr(150), '-')), 'ÁÉÍÓÚÜÑ', 'AEIOUUN'),
        '\s+', ' ', 'g'
    ))
{% endmacro %}

{% macro a_numero(columna) %}
    case when {{ columna }} ~ '^-?[0-9]+(\.[0-9]+)?$' then {{ columna }}::numeric end
{% endmacro %}

{% macro a_fecha(columna) %}
    case when {{ columna }} ~ '^\d{4}-\d{2}-\d{2}' then left({{ columna }}, 10)::date end
{% endmacro %}