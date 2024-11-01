import dlt
from dlt.sources.helpers import requests
import json
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
        dataset_name="sl_announcements"
    )
    # Extract, normalize, and load the data
    load_info = pipeline.run(sl_announcements_resource(), table_name=table_name)
    print(load_info)  # noqa: T201

""" Leave example code for now, will be removed in the future 
@dlt.resource(write_disposition="replace")
def github_api_resource(api_secret_key: Optional[str] = dlt.secrets.value):
    from dlt.sources.helpers.rest_client import paginate
    from dlt.sources.helpers.rest_client.auth import BearerTokenAuth
    from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator

    url = "https://api.github.com/repos/dlt-hub/dlt/issues"
    # Github allows both authenticated and non-authenticated requests (with low rate limits)
    auth = BearerTokenAuth(api_secret_key) if api_secret_key else None
    for page in paginate(
        url, auth=auth, paginator=HeaderLinkPaginator(), params={"state": "open", "per_page": "100"}
    ):
        yield page
"""

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline()
