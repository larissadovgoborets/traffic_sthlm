WITH stg_sl_stop_point_detail AS (SELECT * FROM {{ source('traffic_data_sthlm_db', 'stg_sl_stop_point_info') }}
)

SELECT 
    id,
    name,
    sname,
    type,
    lat,
    lon, 
    stop_area__id as stop_area_key,
    stop_area__name as stop_area_name,


FROM stg_sl_stop_point_detail