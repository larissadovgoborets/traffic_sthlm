WITH stop_point AS (SELECT * FROM {{ ref('src_sl_scope_stop_point') }}),

stop_details AS (SELECT * FROM {{ ref('src_sl_stop_point_detail') }})

SELECT
    stop_point.id as id,
    stop_point.name as name,
    stop_details.type as type,
    lat,
    lon

FROM stop_point
LEFT JOIN stop_details ON stop_point.id = stop_details.id