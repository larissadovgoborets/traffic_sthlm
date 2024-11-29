WITH stg_traffic_messages AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_trafikverket_deviation') }}
)

SELECT
    id as location_id,
    location_descriptor,
    GEOMETRY__POINT__WGS84 as coordinates,  
FROM stg_traffic_messages