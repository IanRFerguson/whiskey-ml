WITH
    base AS (
        SELECT

            {{
                dbt_utils.star(
                    from=ref("stg__setup")
                )
            }}

        FROM {{ ref("stg__setup") }}
    )

SELECT

    dbt_id,
    profile_id,
    standard_styles,
    country_of_origin,
    proof,
    rating,
    review,
    TRIM(note) AS _note_value,
    ROW_NUMBER() OVER (PARTITION BY dbt_id) AS _note_index,
    {{ flavor_categories("TRIM(note)") }} AS _note_quality

FROM base
CROSS JOIN UNNEST(base.flavor_profile) AS note