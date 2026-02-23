import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


@dlt.resource(name="rides")
def nyc_taxi_rides():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    # Endpoint: /data_engineering_zoomcamp_api
    # Pagination: API boş liste döndürdüğünde kendiliğinden duracak
    for page in client.paginate("data_engineering_zoomcamp_api"):
        if not page:      # boş sayfa -> dur
            break
        yield page


pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline_pipeline",
    destination="duckdb",
    refresh="drop_sources",
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(nyc_taxi_rides())
    print(load_info)