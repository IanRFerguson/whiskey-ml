{% macro string_to_array(field, delimiter=',') %}
    ARRAY(
        SELECT * FROM UNNEST(
            SPLIT(
                UPPER({{ field }}), '{{ delimiter }}'
            )
        )
    )
{% endmacro %}