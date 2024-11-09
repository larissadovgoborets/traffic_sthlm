import dlt
import json
import requests
from pathlib import Path
import os
from eda_functions import xml_query
from dotenv import load_dotenv
load_dotenv()

def _get_traffic_data():
    url = 'https://api.trafikinfo.trafikverket.se/v2/data.json'
    headers = {
    'Content-Type': 'application/xml', 
    }
    API_key = os.getenv('API_KEY')
    filter = """<EQ name = "Deleted" value = "false"/>"""
    xml_data = xml_query(API_key=API_key,filter=filter,object_type='TrainAnnouncement')
    response = requests.post(url=url, data=xml_data, headers=headers)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode('utf8'))

@dlt.resource(write_disposition="replace")
def traffic_data_resource():
    response = _get_traffic_data()['RESPONSE']['RESULT'][0]['TrainAnnouncement']
    for data in response:
        yield data

def run_pipeline(table_name):
    pipeline = dlt.pipeline(
    pipeline_name='trafikverket_load',
    destination='snowflake',
    dataset_name='staging',
    )
    
    credentials = {'database':os.getenv('SNOWFLAKE_DATABASE'),
                   'password':os.getenv('SNOWFLAKE_USER_PASSWORD'),
                   'username':os.getenv('SNOWFLAKE_USERNAME'),
                   'host':os.getenv('SNOWFLAKE_HOST'),
                   'warehouse':os.getenv('SNOWFLAKE_WAREHOUSE'),
                   'role':os.getenv('SNOWFLAKE_ROLE')
                   }
    
    load_info = pipeline.run(traffic_data_resource(), table_name=table_name,credentials=credentials)
    print(load_info)

if __name__ == "__main__":
    # specify the pipeline name, destination and dataset name when configuring pipeline,
    # otherwise the defaults will be used that are derived from the current script name
    # data science, data engineer, data analyst
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
    table_name = "data_sthlm_traffic2"
    run_pipeline(table_name)


