WITH src_traffic_deviation_details AS (SELECT * FROM {{ ref('src_traffic_deviation_details') }})


SELECT
    {{ dbt_utils.generate_surrogate_key(['deviation_id','affected_direction']) }} AS deviation_id,
    affected_direction,
    affected_direction_value,
    number_of_lanes_restricted,
    road_number,
    road_number_numeric,
    traffic_restriction_type,
    temporary_limit,
    road_name,
    severity_code,
    severity_text
FROM src_traffic_deviation_details