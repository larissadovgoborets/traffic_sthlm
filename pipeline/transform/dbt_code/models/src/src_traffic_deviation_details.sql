WITH stg_traffic_messages AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_trafikverket_deviation') }}
)


SELECT 
    id as deviation_id,
    affected_direction,
    affected_direction_value,
    number_of_lanes_restricted,
    road_number,
    road_number_numeric,
    traffic_restriction_type,
    temporary_limit,
    road_name,
    severity_code,
    severity_text
FROM stg_traffic_messages