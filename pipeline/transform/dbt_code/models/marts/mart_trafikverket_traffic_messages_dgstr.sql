WITH fct_traffic_msg AS (SELECT * FROM {{ ref('fct_traffic_messages_dgstr') }}),

src_location AS (SELECT * FROM {{ ref('dim_location_dgstr') }}),

src_deviation AS (SELECT * FROM {{ ref('dim_traffic_deviation_details_dgstr') }})

SELECT 
    id,
    header,
    message,
    message_code,
    message_type,
    location_descriptor,
    longitude,
    latitude,
    start_time,
    end_time,
    affected_direction,
    number_of_lanes_restricted,
    road_number,
    road_number_numeric,
    temporary_limit,
    traffic_restriction_type,
    road_name,
    severity_text

FROM 
    fct_traffic_msg 
LEFT JOIN 
    src_location ON fct_traffic_msg.location_id = src_location.location_id
LEFT JOIN 
    src_deviation ON fct_traffic_msg.deviation_id = src_deviation.deviation_id