WITH
    base AS (
        SELECT

            *

        FROM {{ ref("stg__setup") }}
    )

SELECT

    dbt_id,
    profile_id,
    standard_styles,
    country_of_origin,
    proof,
    rating,
    my_review,
    TRIM(note) AS _note_value,
    ROW_NUMBER() OVER (PARTITION BY dbt_id) AS _note_index

FROM base
CROSS JOIN UNNEST(base.flavor_profile) AS note