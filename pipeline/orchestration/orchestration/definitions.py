from dagster import Definitions, load_assets_from_modules, ScheduleDefinition, define_asset_job
from dagster_embedded_elt.dlt import DagsterDltResource

from orchestration import assets  # noqa: TID252

dlt_resource = DagsterDltResource()
all_assets = load_assets_from_modules([assets])
all_assets_job = define_asset_job(name="all_assets_job")

minute_schedule = ScheduleDefinition(
    name="minute_schedule",
    cron_schedule="*/2 * * * *",  # run every minute
    job=all_assets_job,  
)

defs = Definitions(
    assets=all_assets,
    resources={
        "dlt": dlt_resource,
    },
    jobs=[all_assets_job],
    schedules=[minute_schedule],
)