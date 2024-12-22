WITH sl_ann AS (SELECT * FROM {{ ref('src_sl_announcement') }}),

sl_msg AS (SELECT * FROM {{ ref('src_sl_message') }}),

sl_line AS (SELECT * FROM {{ ref('src_sl_scope_line') }}),

sl_stp_area AS (SELECT * FROM {{ ref('src_sl_scope_stop_area') }}),

sl_stp_point AS (SELECT * FROM {{ ref('src_sl_scope_stop_point') }}),

sl_stp_detail AS (SELECT * FROM {{ ref('src_sl_stop_point_detail') }}),


SELECT 
    id,
    {{dbt_utils.generate_surrogate_key(['src_location.location_id','src_location.coordinates'])}} as location_id,
    {{dbt_utils.generate_surrogate_key(['src_deviation.deviation_id', 'src_deviation.affected_direction'])}} as deviation_id,
    COALESCE(header,'ej specificerad') AS header,
    COALESCE(message,'Detaljerad informaion saknas') AS message,
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