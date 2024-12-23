WITH stg_sl_scope_stop_area AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_sl_scope_stop_areas') }}
)

SELECT 
    id,
    name,
    type,
    _dlt_parent_id,
    _dlt_id

FROM stg_sl_scope_stop_area