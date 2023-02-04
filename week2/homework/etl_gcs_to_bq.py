import pandas as pd

from pathlib import Path
from prefect import flow, task, get_run_logger
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("gcp-bucket")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../")
    return Path(f"../{gcs_path}")

@task()
def write_bq(path: Path) -> int:
    """Write DataFrame to BiqQuery and return amount of rows"""

    df = pd.read_parquet(path)
    gcp_credentials_block = GcpCredentials.load("gcp-creds")

    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="de-zoomcamp-2023-375411",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )

    return df.shape[0]


@flow()
def etl_gcs_to_bq(year, month, color):
    """Main EL flow to load data into Big Query
        returns amt of rows downloaded"""

    logger = get_run_logger()

    path = extract_from_gcs(color, year, month)
    rows_amt = write_bq(path)

    logger.info(f'\nRESULT: Rows loaded for year: {year} month: {month}: color {color} -- {rows_amt}\n')

    return rows_amt


@flow()
def etl_parent_flow(
    months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"
):
    logger = get_run_logger()
    rows_amt_list = []

    for month in months:
        rows_amt = etl_gcs_to_bq(year, month, color)
        rows_amt_list.append(rows_amt)
    
    logger.info(f'\n\nRESULT: Rows loaded for year: {year} months: {months}: color {color} -- {rows_amt_list}\nTotal rows loaded: {sum(rows_amt_list)}\n')

if __name__ == "__main__":
    color = "yellow"
    months = [2, 3]
    year = 2019
    etl_parent_flow(months, year, color)
