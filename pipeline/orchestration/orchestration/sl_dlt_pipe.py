import dlt
from dlt.sources.helpers import requests
import os
from pathlib import Path


@dlt.resource(write_disposition="replace", name="sl_announcements")
def sl_announcements_resource():
    url = "https://deviations.integration.sl.se/v1/messages?future=true"
    announcements = requests.get(url).json()
    for announcement in announcements:
        yield announcement

@dlt.resource(write_disposition="replace", name = "sl_stop_point_info")
def stop_point_info_resource():
    stop_points_url = 'https://transport.integration.sl.se/v1/stop-points'
    stop_points = requests.get(stop_points_url).json()
    for stop_point in stop_points:
        yield stop_point

@dlt.source
def sl_announcements_source():
    return sl_announcements_resource(), stop_point_info_resource()

def run_pipeline():
    # Create a pipeline to load data into Snowflake
    pipeline = dlt.pipeline(
        pipeline_name="sl_dlt_pipe", 
        destination='snowflake', 
        dataset_name="staging")
    
    # Extract, normalize, and load the data
    load_info = pipeline.run(sl_announcements_source())
    print(load_info)  

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline()
