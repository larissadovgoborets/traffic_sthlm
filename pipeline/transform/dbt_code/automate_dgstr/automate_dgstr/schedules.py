"""
To add a daily schedule that materializes your dbt assets, uncomment the following lines.
"""
from dagster_dbt import build_schedule_from_dbt_selection
from dagster import ScheduleDefinition

from .assets import dbt_code_dbt_assets
from .jobs import sl_dlt_job, trafikverket_dlt_job


schedules = [
     build_schedule_from_dbt_selection(
         [dbt_code_dbt_assets],
         job_name="materialize_dbt_models",
         cron_schedule="* * * * *",
         dbt_select="fqn:*",
     ),
    ScheduleDefinition(
        name="sl_dlt_every_2min",
        cron_schedule="*/2 * * * *",
        job=sl_dlt_job,
    ),
    ScheduleDefinition(
        name="trafikverket_dlt_every_2min",
        cron_schedule="*/2 * * * *",
        job=trafikverket_dlt_job,
    ),

]
