WITH stg_traffic_messages AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_trafikverket_deviation') }}
)

SELECT 
    id,
    header,
    message_code,
    message_code_value,
    message_type,
    safety_related_message,
    start_time,
    end_time,
    valid_until_further_notice


FROM stg_traffic_messages
