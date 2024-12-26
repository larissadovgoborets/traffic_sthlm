import dlt
from dlt.sources.helpers import requests
import os
from pathlib import Path


@dlt.resource(write_disposition="replace", name="sl_announcements")
def sl_deviations_resource():
    api_url = "https://deviations.integration.sl.se/v1/messages?future=true"
    response = requests.get(api_url)
    response.raise_for_status()
    deviations = response.json()
    for deviation in deviations:
        yield deviation

@dlt.resource(write_disposition="replace", name = "sl_stop_point_info")
def stop_point_info_resource():
    stop_points_url = 'https://transport.integration.sl.se/v1/stop-points'
    response = requests.get(stop_points_url)
    response.raise_for_status()
    stop_points = response.json()
    for stop_point in stop_points:
        yield stop_point

@dlt.source
def sl_deviations_with_coordinates():
    return sl_deviations_resource(), stop_point_info_resource()

def run_pipeline():
    # Create a pipeline to load data into Snowflake
    pipeline = dlt.pipeline(
        pipeline_name="extract_from_sl_pipeline", 
        destination='snowflake', 
        dataset_name="staging")
    
    # Extract, normalize, and load the data
    load_info = pipeline.run(sl_deviations_with_coordinates())
    print(load_info)  

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline()
