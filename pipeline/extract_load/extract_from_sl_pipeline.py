import dlt
from dlt.sources.helpers import requests
import os
from pathlib import Path

def get_sl_announcements():
    """load data from Sl's API"""
    # Extract data from the API
    api_url = "https://deviations.integration.sl.se/v1/messages?future=true"
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def get_station_point_info():
    stop_points_url = 'https://transport.integration.sl.se/v1/stop-points'
    stop_points = requests.get(stop_points_url).json()
    return stop_points

@dlt.resource(write_disposition="replace", name="sl_announcements")
def sl_announcements_resource():
    for announcement in get_sl_announcements():
        yield announcement

@dlt.resource(write_disposition="replace", name = "sl_stop_point_info")
def stop_point_info_resource():
    for stop_point in get_station_point_info():
        yield stop_point

@dlt.source
def sl_announcements_with_coordinates():
    return sl_announcements_resource(), stop_point_info_resource()

def run_pipeline():
    # Create a pipeline to load data into Snowflake
    pipeline = dlt.pipeline(
        pipeline_name="extract_from_sl_pipeline", 
        destination='snowflake', 
        dataset_name="staging")
    
    # Extract, normalize, and load the data
    load_info = pipeline.run(sl_announcements_with_coordinates())
    print(load_info)  

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline()
