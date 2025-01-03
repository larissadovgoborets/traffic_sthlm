from dagster import AssetExecutionContext
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dlt import pipeline
from .load_trafikverket_data_pipeline import traffic_data_source


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
def dagster_situation(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)