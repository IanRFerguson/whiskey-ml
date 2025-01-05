{% macro filter_ratings(field) %}
    {% set complete_records = var('records') == 'complete' %}
    
    {% if complete_records %}
    WHERE {{ field }} IS NOT NULL
    {% endif %}
{% endmacro %}