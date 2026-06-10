{% macro get_year(date_column) %}
    extract(year from {{ date_column }})
{% endmacro %}

{% macro get_month(date_column) %}
    extract(month from {{ date_column }})
{% endmacro %}

{% macro get_week(date_column) %}
    extract(isoweek from {{ date_column }})
{% endmacro %}
