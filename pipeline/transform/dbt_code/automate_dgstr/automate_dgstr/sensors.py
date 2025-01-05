from dagster import RunRequest, DagsterRunStatus, run_status_sensor
from .jobs import sl_dlt_job, sl_dbt_job, trafikverket_dlt_job, trafikverket_dbt_job


@run_status_sensor(run_status=DagsterRunStatus.SUCCESS, 
                   minimum_interval_seconds=90,
                   monitored_jobs=[sl_dlt_job], request_job=sl_dbt_job)
def sl_dlt_success_sensor(context):
    run_key = f"sl_dbt_job_triggered_{context.dagster_run.run_id}"
    return RunRequest(run_key=run_key)


@run_status_sensor(run_status=DagsterRunStatus.SUCCESS, 
                   minimum_interval_seconds=90,
                   monitored_jobs=[trafikverket_dlt_job], request_job=trafikverket_dbt_job)
def trafikverket_dlt_success_sensor(context):
    run_key = f"trafikverket_dbt_job_triggered_{context.dagster_run.run_id}"
    return RunRequest(run_key=run_key)
