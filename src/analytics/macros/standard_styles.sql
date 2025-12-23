{% macro standard_styles(field) %}
CASE
    WHEN UPPER({{ field }}) LIKE '%RYE%'
        THEN 'RYE'
    WHEN UPPER({{ field }}) LIKE '%BOURBON%'
        THEN 'BOURBON'
    WHEN UPPER({{ field }}) LIKE '%IRISH%'
        THEN 'WHISKEY - IRISH'
    ELSE 'WHISKEY - OTHER'
END
{% endmacro %}