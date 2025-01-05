from dagster import (
    load_assets_from_modules, define_asset_job, 
    AssetSelection)

from automate_dgstr import assets

all_assets = load_assets_from_modules([assets])

sl_dlt_job = define_asset_job(name="sl_dlt_job", 
                                       selection=AssetSelection.keys("dlt_sl_deviations_source_sl_deviations", 
                                                                     "dlt_sl_deviations_source_sl_stop_point_info"))

sl_dbt_job = define_asset_job(name="sl_dbt_job", 
                                         selection=AssetSelection.keys("warehouse/fct_sl_deviation_dgstr", 
                                                                       "warehouse/dim_sl_stop_point_dgstr",
                                                                       "warehouse/dim_sl_line_dgstr",
                                                                       "warehouse/dim_sl_stop_area_dgstr",
                                                                       "marts/mart_sl_deviations_dgstr"))


trafikverket_dlt_job = define_asset_job(name="trafikverket_dlt_job", 
                                                 selection=AssetSelection.keys("dlt_traffic_data_source_traffic_data_resource"))

trafikverket_dbt_job = define_asset_job(name="trafikverket_dbt_job",
                                             selection=AssetSelection.keys("warehouse/fct_traffic_messages_dgstr",
                                                                            "warehouse/dim_traffic_deviation_details_dgstr",
                                                                            "warehouse/dim_location_dgstr",
                                                                            "marts/mart_trafikverket_traffic_messages_dgstr"))







