WITH src_dim_location AS (SELECT * FROM {{ ref('src_dim_location') }})


SELECT
    {{ dbt_utils.generate_surrogate_key(['location_id','coordinates']) }} AS location_id,
    location_descriptor,
    coordinates
FROM src_dim_location