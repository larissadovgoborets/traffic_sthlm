WITH stop_area AS (SELECT * FROM {{ ref('src_sl_scope_stop_area') }}),

stop_details AS (SELECT * FROM {{ ref('src_sl_stop_point_detail') }})

SELECT
    stop_area.id as stop_area_id,
    stop_area.name as name,
    stop_area.type as type,
    AVG(lat) as lat,
    AVG(lon) as lon

FROM stop_area
LEFT JOIN stop_details ON stop_area.id = stop_details.stop_area_key
GROUP BY stop_area_id, stop_area.name, stop_area.type