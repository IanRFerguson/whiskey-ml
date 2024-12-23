WITH
    analytics AS (
        SELECT
        
            dbt_id,
            profile_id,
            rating,
            predicted_rating

        FROM {{ ref("prd__analytics") }}
    )

SELECT

    _stg.dbt_id,
    _stg.profile_id,
    _stg.maker,
    _stg.name,
    _stg.style,
    _stg.standard_styles,
    _stg.country_of_origin,
    _stg.proof,
    _stg.rating,
    AVG(_prd.predicted_rating) AS average_predicted_rating,
    MIN(_prd.predicted_rating) AS minimum_predicted_rating,
    MAX(_prd.predicted_rating) AS maximum_predicted_rating,
    (_stg.rating - AVG(_prd.predicted_rating)) AS actual_vs_predicted,
    _stg.my_review,
    _stg.flavor_profile

FROM {{ ref("stg__setup") }} AS _stg
LEFT JOIN analytics AS _prd USING(dbt_id)
GROUP BY ALL