WITH fct_sl AS (SELECT * FROM {{ ref('fct_sl_deviation') }}),

dim_line AS (SELECT * FROM {{ ref('dim_sl_line') }}),

dim_stop_area AS (SELECT * FROM {{ ref('dim_sl_stop_area') }}),

dim_stop_point AS (SELECT * FROM {{ ref('dim_sl_stop_point') }})

SELECT
    deviation_case_id,
    publish_from,
    publish_upto,
    header,
    message,
    priority,
    scope_alias,
    line_key,
    dim_line.name as line_name,
    transport_mode,
    dim_stop_area.name as stop_area_name,
    dim_stop_point.name as stop_point_name,
    CASE 
        WHEN dim_stop_point.name IS NULL THEN dim_stop_area.lat
        ELSE dim_stop_point.lat
    END AS lat,
    CASE 
        WHEN dim_stop_point.name IS NULL THEN dim_stop_area.lon
        ELSE dim_stop_point.lon
    END AS lon

FROM fct_sl
LEFT JOIN dim_line ON fct_sl.line_key = dim_line.line_id
LEFT JOIN dim_stop_area ON fct_sl.stop_area_key = dim_stop_area.stop_area_id
LEFT JOIN dim_stop_point ON fct_sl.stop_point_key = dim_stop_point.id