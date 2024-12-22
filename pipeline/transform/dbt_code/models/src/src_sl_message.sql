WITH stg_sl_message AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_sl_messages') }}
)

SELECT 
    _dlt_parent_id,
    header,
    details,
    scope_alias,
    _dlt_id


FROM stg_sl_message