from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets

from dlt import pipeline
from .load_trafikverket_data_pipeline import traffic_data_source
from .sl_dlt_pipe import sl_deviations_source
from .project import dbt_code_project

@dlt_assets(
    dlt_source=traffic_data_source(),

    dlt_pipeline=pipeline(
        pipeline_name='trafikverket_load',
        destination='snowflake',
        dataset_name='staging',
        progress="log"
    ),
    name="trafikverket",
)
def stg_situation(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

@dlt_assets(
    dlt_source=sl_deviations_source(),

    dlt_pipeline=pipeline(
        pipeline_name="sl_dlt_pipe",
        destination='snowflake',
        dataset_name="staging",
        progress="log"
    ),
    name="sl",
)
def stg_deviations(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

@dbt_assets(manifest=dbt_code_project.manifest_path)
def dbt_code_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

 