WITH src_dim_location AS (SELECT * FROM {{ ref('src_location') }})


SELECT
    {{ dbt_utils.generate_surrogate_key(['location_id','coordinates']) }} AS location_id,
    COALESCE(location_descriptor, 'ej specificerad') AS location_descriptor,
    coordinates
FROM src_dim_location