# NYC Taxi dlt Pipeline

This project implements a small data pipeline using the **dlt** library to ingest NYC Taxi trip data from a REST API into **DuckDB** for analysis.

The pipeline was built as part of the DataTalksClub **Data Engineering Zoomcamp** dlt workshop homework.

---

## Project Overview

- **Source**: Custom NYC Taxi API exposed for the Zoomcamp  
- **Base URL**: `https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api`  
- **Format**: Paginated JSON, 1,000 records per page  
- **Destination**: Local DuckDB database file `taxi_pipeline_pipeline.duckdb`  
- **Main table**: `taxi_pipeline_pipeline_dataset.rides`  

Each row in `rides` represents a single taxi trip and contains fields such as pickup and dropoff timestamps, trip distance, fares, tips and payment type.[web:119]

---

## Pipeline Implementation

The core pipeline is defined in `taxi_pipeline_pipeline.py` and uses dlt’s `RESTClient` with a page-number paginator.

Key elements:

```python
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator

@dlt.resource(name="rides")
def nyc_taxi_rides():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None,
        ),
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):
        if not page:
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
This configuration automatically walks through all available pages until the API returns an empty page and loads the results into DuckDB.[web:119]

How to Run
Create and activate the environment (managed by uv):

bash
uv sync
Run the dlt pipeline:

bash
uv run python taxi_pipeline_pipeline.py
This will:

Call the NYC Taxi API,

Extract all pages of data (10,000+ rows),

Normalize them, and

Load them into taxi_pipeline_pipeline.duckdb under the schema taxi_pipeline_pipeline_dataset.[web:119]

Inspect the DuckDB database:

bash
uv run python
python
import duckdb
con = duckdb.connect(r"taxi_pipeline_pipeline.duckdb")

# Preview data
print(con.sql("""
    SELECT *
    FROM taxi_pipeline_pipeline_dataset.rides
    LIMIT 5
""").df())
Schema
taxi_pipeline_pipeline_dataset.rides contains the following key columns:

trip_pickup_date_time (timestamp with time zone)

trip_dropoff_date_time (timestamp with time zone)

trip_distance (double)

fare_amt, tip_amt, tolls_amt, total_amt, surcharge (double)

payment_type (varchar, e.g. Credit, CASH)

passenger_count (bigint)

start_lat, start_lon, end_lat, end_lon (double)

_dlt_load_id, _dlt_id (technical columns added by dlt)

These fields are enough to answer basic analytics questions such as time coverage, payment mix, and total tip revenue.[web:119]

Example Analysis Queries
All queries target the rides table in the taxi_pipeline_pipeline_dataset schema.

Date range of the dataset

sql
SELECT
    MIN(trip_pickup_date_time) AS min_pickup_ts,
    MAX(trip_pickup_date_time) AS max_pickup_ts
FROM taxi_pipeline_pipeline_dataset.rides;
Share of trips paid by credit card

sql
SELECT
    COUNT(*) AS total_trips,
    SUM(CASE WHEN payment_type = 'Credit' THEN 1 ELSE 0 END) AS credit_trips,
    100.0 * SUM(CASE WHEN payment_type = 'Credit' THEN 1 ELSE 0 END) / COUNT(*) AS credit_share_pct
FROM taxi_pipeline_pipeline_dataset.rides;
Total tip amount

sql
SELECT
    ROUND(SUM(tip_amt), 2) AS total_tip_amount
FROM taxi_pipeline_pipeline_dataset.rides;
These queries were used to answer the homework questions about the dataset coverage, payment distribution, and total tip revenue.

Future Improvements
Potential next steps for this project:

Parameterize the API call by date range or taxi type.

Schedule the pipeline with a workflow orchestrator (e.g. Prefect or Airflow).

Build a downstream analytics layer with dbt on top of the DuckDB tables.
