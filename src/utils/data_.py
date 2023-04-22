import s3fs
from pandas import (
    read_csv,
    DataFrame
)


def import_from_S3(
        endpoint: str,
        bucket: str,
        path: str,
        key_id: str,
        access_key: str,
        token: str) -> DataFrame:
    """
    enabling conexion to s3 storage for data retrieving
    """
    fs = s3fs.S3FileSystem(
            client_kwargs={'endpoint_url': endpoint},
            key=key_id,
            secret=access_key,
            token=token)

    return read_csv(
                fs.open(f"{bucket}/{path}/online_retail_data.csv"),
            )


def import_from_local(path) -> DataFrame:
    return read_csv(
                f"{path}/data/online_retail_data.csv",
                encoding="utf-8").set_index("Customer_ID")
