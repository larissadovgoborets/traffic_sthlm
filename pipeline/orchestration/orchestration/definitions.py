from dagster import Definitions, load_assets_from_modules, ScheduleDefinition, define_asset_job, AssetSelection 
from dagster_embedded_elt.dlt import DagsterDltResource

from orchestration import assets  # noqa: TID252

dlt_resource = DagsterDltResource()
all_assets = load_assets_from_modules([assets])
all_assets_job = define_asset_job(name="all_assets_job", selection=AssetSelection.all())

sl_job = define_asset_job(
    name="sl_job",
    selection=AssetSelection.keys("dlt_sl_announcements_source_sl_announcements1", 
                                  "dlt_sl_announcements_source_sl_stop_point_info"),
)

minute_schedule = ScheduleDefinition(
    name="minute_schedule",
    cron_schedule="*/2 * * * *",  # run every minute
    job=sl_job,  
)

defs = Definitions(
    assets=all_assets,
    resources={
        "dlt": dlt_resource,
    },
    jobs=[all_assets_job, sl_job],
    schedules=[minute_schedule],
)
