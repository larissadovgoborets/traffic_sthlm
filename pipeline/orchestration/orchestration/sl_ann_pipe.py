import dlt
from dlt.sources.helpers import requests
import os
from pathlib import Path

@dlt.resource(write_disposition="replace", name="sl_deviations")
def sl_deviation_resource():    
    deviations_url = "https://deviations.integration.sl.se/v1/messages?future=true"
    deviations = requests.get(deviations_url)
    deviations.raise_for_status()
    for deviation in deviations.json:
        yield deviation

@dlt.source
def sl_deviation_source():
    return sl_deviation_resource()

def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="sl_deviation_pipe", 
        destination='snowflake', 
        dataset_name="staging")
    
    load_info = pipeline.run(sl_deviation_source())
    print(load_info)

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline()