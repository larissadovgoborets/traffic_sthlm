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

@dlt.resource(write_disposition="replace")
def sl_announcements_resource():
    for announcement in get_sl_announcements():
        yield announcement

def run_pipeline(table_name="sl_announcements"):
    # Create a pipeline to load data into Snowflake
    pipeline = dlt.pipeline(
        pipeline_name="extract_from_sl_pipeline", 
        destination='snowflake', 
        dataset_name="staging")
    
    # Extract, normalize, and load the data
    load_info = pipeline.run(sl_announcements_resource(), table_name=table_name)
    print(load_info)  

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline()
