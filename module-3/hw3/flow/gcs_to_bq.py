from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(year: int, month: int) -> Path:
    """Download trip data from GCS"""

    # afro-prefect-de/data/fhv

    gcs_path = f"data/fhv/fhv_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("afro-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task()
def read_from_gcs(path: Path) -> pd.DataFrame:
    """Read file from GCS"""
    df = pd.read_parquet(path)
    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("afro-prefect-creds")

    df.to_gbq(
        destination_table="afro.fhv",
        project_id="afro-de-376122",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq(year: int, month: int) -> int:
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(year, month)
    df = read_from_gcs(path)
    write_bq(df)
    return len(df)


@flow(log_prints=True)
def etl_parent_flow(months: list[int] = [i for i in range(1, 13)], year: int = 2019):
    for month in months:
        rows = etl_gcs_to_bq(year, month)
        print(f"year: {year}, month: {month}, rows: {rows}")


if __name__ == "__main__":
    months = [i for i in range(1, 13)]
    year = 2019
    etl_parent_flow(months, year)
