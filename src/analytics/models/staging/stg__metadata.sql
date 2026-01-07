WITH
    base AS (
        SELECT

            {{
                dbt_utils.star(
                    from=ref("stg__setup")
                )
            }}

        FROM {{ ref("stg__setup") }}
    ),

    average_by_year AS (
        SELECT

            source_year,
            AVG(rating) AS average_rating_by_year

        FROM base
        GROUP BY source_year
    )

SELECT

    dbt_id,
    profile_id,
    source_year,
    standard_styles,
    country_of_origin,
    proof,
    rating,
    average_rating_by_year,
    review,
    TRIM(note) AS _note_value,
    ROW_NUMBER() OVER (PARTITION BY dbt_id) AS _note_index,
    {{ flavor_categories("TRIM(note)") }} AS _note_quality

FROM base
JOIN average_by_year USING(source_year)
CROSS JOIN UNNEST(base.flavor_profile) AS note