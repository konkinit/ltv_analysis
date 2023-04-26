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


def get_customer_history_data(
        data_summary: DataFrame,
        customer_id: Union[int, float, str],
        n_period: int) -> DataFrame:
    df_ = DataFrame(
                dict(
                    Customer_ID=full(
                                n_period,
                                customer_id,
                                dtype="int"
                            ),
                    frequency=full(
                                n_period,
                                data_summary.loc[customer_id][
                                    RawFeatures.frequency],
                                dtype="int"
                            ),
                    recency=full(
                                n_period,
                                data_summary.loc[customer_id][
                                    RawFeatures.recency
                                ]
                            ),
                    T=(
                        arange(-1, n_period-1)+data_summary.loc[customer_id][
                            RawFeatures.T
                        ]).astype("int"),
                ))
    df_.columns = [
        RawFeatures.CUSTOMER_ID,
        RawFeatures.frequency,
        RawFeatures.recency,
        RawFeatures.T
    ]
    return df_


def get_customer_whatif_data(
        data_summary: DataFrame,
        customer_id: Union[int, float, str],
        n_period: int,
        T_future_transac: int) -> DataFrame:
    history_ = get_customer_history_data(
                    data_summary,
                    customer_id,
                    n_period
                )
    history_[RawFeatures.frequency].iloc[-T_future_transac:] += 1
    history_[RawFeatures.recency].iloc[-T_future_transac:] = history_[
        RawFeatures.T].iloc[-T_future_transac] - 0.5
    return history_
