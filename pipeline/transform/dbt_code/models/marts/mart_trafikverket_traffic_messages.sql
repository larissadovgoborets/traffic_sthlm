WITH fct_traffic_msg AS (SELECT * FROM {{ ref('fct_traffic_messages') }}),

src_location AS (SELECT * FROM {{ ref('dim_location') }}),

src_deviation AS (SELECT * FROM {{ ref('dim_traffic_deviation_details') }})

SELECT 
    id,
    header,
    message_code,
    message_type,
    safety_related_message,
    location_descriptor,
    coordinates,
    start_time,
    end_time

FROM 
    fct_traffic_msg 
LEFT JOIN 
    src_location ON fct_traffic_msg.location_id = src_location.location_id
LEFT JOIN 
    src_deviation ON fct_traffic_msg.deviation_id = src_deviation.deviation_id