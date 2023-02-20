from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta


# task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
@task(retries=3, log_prints=True)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
    #     raise Exception
    print(dataset_url, end='\n')
    df = pd.read_csv(dataset_url, low_memory=False, encoding='latin1', compression='gzip')
    # df = pd.read_csv(dataset_url)

    return df


@task(log_prints=True)
def clean(color: str, df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    if color == "yellow":
        """Fix dtype issues"""
        df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
        df["tpep_dropoff_datetime"] = pd.to_datetime(
            df["tpep_dropoff_datetime"])

    if color == "green":
        """Fix dtype issues"""
        df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
        df["lpep_dropoff_datetime"] = pd.to_datetime(
            df["lpep_dropoff_datetime"])
        df["trip_type"] = df["trip_type"].astype('Int64')

    if color == "yellow" or color == "green":
        df["VendorID"] = df["VendorID"].astype('Int64')
        df["RatecodeID"] = df["RatecodeID"].astype('Int64')
        df["PULocationID"] = df["PULocationID"].astype('Int64')
        df["DOLocationID"] = df["DOLocationID"].astype('Int64')
        df["passenger_count"] = df["passenger_count"].astype('Int64')
        df["payment_type"] = df["payment_type"].astype('Int64')

    if color == "fhv":
        """Rename columns"""
        df.rename({'dropoff_datetime': 'dropOff_datetime'},
                  axis='columns', inplace=True)
        df.rename({'PULocationID': 'PUlocationID'},
                  axis='columns', inplace=True)
        df.rename({'DOLocationID': 'DOlocationID'},
                  axis='columns', inplace=True)

        # df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
        # df["dropOff_datetime"] = pd.to_datetime(df["dropOff_datetime"])
        # df["PUlocationID"] = pd.array(df["PUlocationID"], dtype="Int64")
        # df["DOlocationID"] = pd.array(df["DOlocationID"], dtype="Int64")
        # df["SR_Flag"] = df["SR_Flag"].astype(str)
        # df["Affiliated_base_number"] = df["Affiliated_base_number"].astype(str)

        """Fix dtype issues"""
        df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
        df["dropOff_datetime"] = pd.to_datetime(df["dropOff_datetime"])

        # See https://pandas.pydata.org/docs/user_guide/integer_na.html
        df["PUlocationID"] = df["PUlocationID"].astype('Int64')
        df["DOlocationID"] = df["DOlocationID"].astype('Int64')
        df["SR_Flag"] = df["SR_Flag"].astype(str)

    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")

    return df


@task()
def write_local(color: str, df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    # path = Path(f"data/fhv/{dataset_file}.parquet")
    # df.to_parquet(path, compression="gzip")

    Path(f"data/dbt/{color}").mkdir(parents=True, exist_ok=True)
    path = Path(f"data/dbt/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")

    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("afro-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow()
def data_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"
    # dataset_file = f"fhv_tripdata_{year}-{month:02}"
    # dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"
    # # https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz

    df = fetch(dataset_url)
    df_clean = clean(color, df)
    path = write_local(color, df_clean, dataset_file)

    write_gcs(path)


@flow()
def etl_parent_flow(colors: list[str] = ["green", "yellow"], months: list[int] = [1, 2], years: list[int] = [2021]):
    for color in colors:
        for year in years:
            for month in months:
                data_to_gcs(year, month, color)


if __name__ == "__main__":
    colors = ["fhv", "green", "yellow"]
    months = [i for i in range(1, 13)]
    years = [2019, 2020]
    etl_parent_flow(colors, months, years)
