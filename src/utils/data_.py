import os
import sys
import s3fs
from numpy import full, arange
from pandas import (
    read_csv,
    DataFrame
)
from typing import Union
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import (
    RawFeatures
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
                encoding='unicode_escape'
            )


def import_from_local(path) -> DataFrame:
    return read_csv(
                f"{path}/data/online_retail_data.csv",
                encoding='unicode_escape'
            ).set_index("Customer_ID")


def get_customer_scoring_data(
        data_summary: DataFrame,
        customer_id: Union[int, float, str],
        n_period: int) -> DataFrame:
    return DataFrame(
                dict(
                    Customer_ID=full(
                                10,
                                customer_id,
                                dtype="int"
                            ),
                    frequency=full(
                                10,
                                data_summary.loc[customer_id][
                                    RawFeatures.frequency],
                                dtype="int"
                            ),
                    recency=full(
                                10,
                                data_summary.loc[customer_id][
                                    RawFeatures.recency
                                ]
                            ),
                    T=(
                        arange(-1, 9)+data_summary.loc[customer_id][
                            RawFeatures.T
                        ]).astype("int"),
                ))
