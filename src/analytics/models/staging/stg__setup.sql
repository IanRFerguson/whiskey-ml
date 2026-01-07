WITH
    base_2024 AS (
        SELECT

            {{
                dbt_utils.star(
                    from=source("raw", "whiskey_2024")
                )
            }},
            CAST(NULL AS STRING) AS distinct_feature -- Placeholder for alignment with 2025 schema

        FROM {{ source("raw", "whiskey_2024") }}
    ),

    base_2025 AS (
        SELECT

            {{
                dbt_utils.star(
                    from=source("raw", "whiskey_2025")
                )
            }}

        FROM {{ source("raw", "whiskey_2025") }}
    ),

    base AS (
        SELECT
            id,
            maker,
            name,
            style,
            distinct_feature,
            country_of_origin,
            proof,
            my_rating,
            my_review,
            profile,
            2024 AS source_year
        FROM base_2024
        
        UNION ALL

        SELECT
            id,
            maker,
            name,
            style,
            distinct_feature,
            country_of_origin,
            proof,
            my_rating,
            my_review,
            profile,
            2025 AS source_year
        FROM base_2025
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
    {{ string_to_array('profile') }} AS flavor_profile,
    source_year

FROM base
{{ filter_ratings("my_rating") }}