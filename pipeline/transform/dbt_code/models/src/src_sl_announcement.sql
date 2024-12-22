WITH stg_sl_announcement AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_sl_announcements') }}
)

SELECT 
    deviation_case_id,
    version,
    created,
    publish__from as publish_from,
    publish__upto as publish_upto,
    priority__importance_level as priority,
    _dlt_id

FROM stg_sl_announcement
