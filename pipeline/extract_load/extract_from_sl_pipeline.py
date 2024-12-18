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

def get_station_coordinates(announcement):
    try: 
        station = announcement['scope']['stop_areas'][0]['name']
        station_data = requests.get(f"https://journeyplanner.integration.sl.se/v1/typeahead.json?searchstring={station}&stationsonly=true&maxresults=1&key=TRAFIKLAB-SLAPI-INTEGRATION-2024")
        station_data = station_data.json()
        lon = station_data['ResponseData'][0]['X']
        lon = int(lon) / 10**(len(lon)-2) # Convert to decimal degrees
        lat = station_data['ResponseData'][0]['Y']
        lat = int(lat) / 10**(len(lat)-2) # Convert to decimal degrees
        station_coordinates = (lat, lon)    
    except KeyError:
        station_coordinates = None
    return station_coordinates

@dlt.resource(write_disposition="replace")
def sl_announcements_resource():
    for announcement in get_sl_announcements():
        yield announcement

@dlt.resource(write_disposition="replace")
def coordinates_resource():
    for announcement in get_sl_announcements():
        station_coordinates = get_station_coordinates(announcement)
        yield station_coordinates

@dlt.source
def sl_announcements_with_coordinates():
    return sl_announcements_resource(), coordinates_resource()

def run_pipeline(table_name="sl_test_announcements"):
    # Create a pipeline to load data into Snowflake
    pipeline = dlt.pipeline(
        pipeline_name="extract_from_sl_pipeline", 
        destination='snowflake', 
        dataset_name="staging")
    
    # Extract, normalize, and load the data
    load_info = pipeline.run(sl_announcements_with_coordinates(), table_name=table_name)
    print(load_info)  

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline()
