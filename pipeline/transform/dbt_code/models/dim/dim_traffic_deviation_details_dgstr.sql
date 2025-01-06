WITH src_traffic_deviation_details AS (SELECT * FROM {{ ref('src_traffic_deviation_details') }})


SELECT
    {{ dbt_utils.generate_surrogate_key(['deviation_id','affected_direction']) }} AS deviation_id,
    affected_direction,
    affected_direction_value,
    COALESCE(number_of_lanes_restricted, 0) AS number_of_lanes_restricted,
    COALESCE(road_number, 'ej specificerad') AS road_number,
    COALESCE(road_number_numeric,0) AS road_number_numeric,
    COALESCE(traffic_restriction_type,'ej specificerad') AS traffic_restriction_type,
    COALESCE(temporary_limit,'Hastighetsbegränsning är ej specificerad') AS temporary_limit,
    COALESCE(road_name, 'ej specificerad') AS road_name,
    COALESCE(severity_code,0) AS severity_code,
    COALESCE(severity_text, 'Påverkans grad saknas') AS severity_text
FROM src_traffic_deviation_details