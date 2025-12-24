WITH
    analytics AS (
        SELECT
        
            dbt_id,
            _z_rating,
            _predicted_z_rating

        FROM {{ ref("ml__rating_predictions") }}
    ),

    clusters AS (
        SELECT
        
            dbt_id,
            _cluster_label AS cluster_label

        FROM {{ ref("ml__clusters") }}
    ),

    semantic_analysis AS (
        SELECT
        
            dbt_id,
            review_sentiment,
            semantic_score

        FROM {{ ref("ml__semantic_analysis") }}
    )

SELECT

    _stg.dbt_id,
    _stg.profile_id,
    _stg.source_year,
    _stg.maker,
    _stg.name,
    _stg.style,
    _stg.standard_styles,
    _stg.country_of_origin,
    _stg.proof,
    _prd._z_rating,
    AVG(_prd._predicted_z_rating) AS average_predicted_z_rating,
    MIN(_prd._predicted_z_rating) AS minimum_predicted_z_rating,
    MAX(_prd._predicted_z_rating) AS maximum_predicted_z_rating,
    (_prd._z_rating - AVG(_prd._predicted_z_rating)) AS actual_vs_predicted,
    _stg.review,
    _stg.flavor_profile,
    _clusters.cluster_label,
    _sem.review_sentiment,
    _sem.semantic_score

FROM {{ ref("stg__setup") }} AS _stg
LEFT JOIN analytics AS _prd USING(dbt_id)
LEFT JOIN clusters AS _clusters USING(dbt_id)
LEFT JOIN semantic_analysis AS _sem USING(dbt_id)
GROUP BY ALL