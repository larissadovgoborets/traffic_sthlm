WITH stg_sl_scope_line AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_sl_scope_lines') }}
)

SELECT 
    id,
    transport_mode,
    group_of_lines,
    name,
    _dlt_parent_id


FROM stg_sl_scope_line