WITH sl_ann AS (SELECT * FROM {{ ref('src_sl_announcement') }}),

sl_msg AS (SELECT * FROM {{ ref('src_sl_message') }}),

sl_line AS (SELECT * FROM {{ ref('src_sl_scope_line') }}),

sl_stp_area AS (SELECT * FROM {{ ref('src_sl_scope_stop_area') }}),

sl_stp_point AS (SELECT * FROM {{ ref('src_sl_scope_stop_point') }}),

sl_stp_detail AS (SELECT * FROM {{ ref('src_sl_stop_point_detail') }})


SELECT 

    {{dbt_utils.generate_surrogate_key(['sl_ann.deviation_case_id', 'sl_ann.version'])}} as announcement_id,
    sl_ann.deviation_case_id as deviation_case_id,
    version,
    created,
    publish_from,
    publish_upto,
    header,
    details as message,
    priority,
    scope_alias,
    sl_line.id as line_key,
    sl_stp_area.id as stop_area_key,
    sl_stp_point.id as stop_point_key

FROM 
    sl_ann
LEFT JOIN 
    sl_msg ON sl_ann._dlt_id = sl_msg._dlt_parent_id
LEFT JOIN 
    sl_line ON sl_ann._dlt_id = sl_line._dlt_parent_id
LEFT JOIN sl_stp_area ON sl_ann._dlt_id = sl_stp_area._dlt_parent_id
LEFT JOIN sl_stp_point ON sl_ann._dlt_id = sl_stp_point._dlt_root_id