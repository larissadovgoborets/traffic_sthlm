WITH stg_sl_scope_stop_point AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_sl_scope_stop_points') }}
)

SELECT 
    id,
    name,
    _dlt_parent_id

FROM stg_sl_scope_stop_point