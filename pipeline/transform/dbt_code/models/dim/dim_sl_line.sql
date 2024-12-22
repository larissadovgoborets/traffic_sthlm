WITH sl_line AS (SELECT * FROM {{ ref('src_sl_scope_line') }})


SELECT
    id as line_id,
    name,
    transport_mode,
    group_of_lines

FROM sl_line