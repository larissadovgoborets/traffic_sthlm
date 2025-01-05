import dlt
import json
import requests
from pathlib import Path
import os
from .eda_functions import xml_query


def _get_traffic_data():
    url = 'https://api.trafikinfo.trafikverket.se/v2/data.json'
    headers = {
    'Content-Type': 'application/xml', 
    }
    API_key = os.getenv('API_KEY')
    filter = """<EQ name = "Deleted" value = "false"/>"""
    xml_data = xml_query(API_key=API_key,filter=filter,object_type='Situation')
    response = requests.post(url=url, data=xml_data, headers=headers)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode('utf8'))

@dlt.resource(write_disposition="replace", table_name="Situation_test")
def traffic_data_resource():
    response = _get_traffic_data()['RESPONSE']['RESULT'][0]['Situation']
    for data in response:
        yield data

@dlt.source
def traffic_data_source():
    return traffic_data_resource()

def run_pipeline():
    pipeline = dlt.pipeline(
    pipeline_name='trafikverket_load',
    destination='snowflake',
    dataset_name='staging',
    )
        
    load_info = pipeline.run(traffic_data_source())
    print(load_info)

if __name__ == "__main__":
    # specify the pipeline name, destination and dataset name when configuring pipeline,
    # otherwise the defaults will be used that are derived from the current script name
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
    run_pipeline()
    


