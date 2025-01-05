from dagster import Definitions, load_assets_from_modules
from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_dbt import DbtCliResource
from automate_dgstr import assets
from .project import dbt_code_project
from .schedules import schedules
from .sensors import sl_dlt_success_sensor, trafikverket_dlt_success_sensor

dlt_resource = DagsterDltResource()
dbt_resource = DbtCliResource(
    project_dir=dbt_code_project,
)

all_assets = load_assets_from_modules([assets])  

defs = Definitions(
    assets=all_assets,
    sensors=[sl_dlt_success_sensor, trafikverket_dlt_success_sensor],
    schedules=schedules,
    resources={
        "dlt": dlt_resource,
        "dbt": dbt_resource,
    },
)
