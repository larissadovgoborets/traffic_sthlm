WITH fct_traffic_msg AS (SELECT * FROM {{ ref('src_fct_traffic_message') }}),

src_location AS (SELECT * FROM {{ ref('src_location') }}),

src_deviation AS (SELECT * FROM {{ ref('src_traffic_deviation_details') }})

SELECT 
    id,
    {{dbt_utils.generate_surrogate_key(['src_location.location_id','src_location.coordinates'])}} as location_id,
    {{dbt_utils.generate_surrogate_key(['src_deviation.deviation_id', 'src_deviation.affected_direction'])}} as deviation_id,
    COALESCE(header,'ej specificerad') AS header,
    message_code,
    message_code_value,
    message_type,
    safety_related_message,
    start_time,
    end_time,
    valid_until_further_notice

FROM 
    fct_traffic_msg 
LEFT JOIN 
    src_location ON fct_traffic_msg.id = src_location.location_id
LEFT JOIN 
    src_deviation ON fct_traffic_msg.id = src_deviation.deviation_id