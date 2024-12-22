WITH stg_sl_announcement AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_sl_announcements') }}
)

SELECT 
    deviation_case_id,
    created,
    publish__from,
    publish__upto,
    _dlt_id

FROM stg_sl_announcement
