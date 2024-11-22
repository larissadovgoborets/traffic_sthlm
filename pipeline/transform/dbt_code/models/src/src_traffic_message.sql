WITH stg_traffic_messages AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_trafikverket_traffic_messages') }}
)

SELECT *
FROM stg_traffic_messages
