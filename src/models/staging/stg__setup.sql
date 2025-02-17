WITH
    base AS (
        SELECT

            *

        FROM {{ source("raw", "whiskey_source_data") }}
    )

SELECT

    {{ dbt_utils.generate_surrogate_key(['id', 'maker', 'name']) }} AS dbt_id,
    id AS profile_id,
    maker,
    name,
    style,
    {{ standard_styles('style') }} AS standard_styles,
    country_of_origin,
    CAST(proof AS FLOAT64) AS proof,
    CAST(my_rating AS FLOAT64) AS rating,
    my_review AS review,
    {{ string_to_array('profile') }} AS flavor_profile

FROM base
{{ filter_ratings("my_rating") }}