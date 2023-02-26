from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("afro-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task()
def get_from_gcs(path: Path) -> pd.DataFrame:
    """Get file from GCS"""
    return pd.read_parquet(path)


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("afro-prefect-creds")

    df.to_gbq(
        destination_table="afro.taxis",
        project_id="afro-de-376122",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def el_gcs_to_bq(year: int, month: int, color: str) -> int:
    """Main ETL flow to load data into Big Query modded to take params"""

    path = extract_from_gcs(color, year, month)
    df = get_from_gcs(path)
    write_bq(df)
    return df.shape[0]


@flow(log_prints=True)
def el_parent_flow(months: list[int] = [2, 3], year: int = 2019, color: str = "yellow"):
    for month in months:
        num_rows = el_gcs_to_bq(year, month, color)
        print(f"month: {month}, year: {year}, rows: {num_rows}")


if __name__ == "__main__":
    color = "yellow"
    months = [2, 3]
    year = 2019
    el_parent_flow()
