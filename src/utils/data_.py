import os
import sys
import s3fs
from numpy import full, arange
from pandas import (
    read_csv,
    DataFrame
)
from typing import Union, Tuple
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
        n_period_: int) -> Tuple[int, DataFrame]:
    # adapt the value of T
    T_ = int(data_summary.loc[customer_id][RawFeatures.T])
    frequency_ = int(data_summary.loc[customer_id][RawFeatures.frequency])
    recency_ = int(data_summary.loc[customer_id][RawFeatures.recency])
    n_period = int(T_ - recency_ + 2 + n_period_)
    df_ = DataFrame(
                dict(
                    Customer_ID=full(
                                n_period,
                                customer_id,
                                dtype="int"
                            ),
                    frequency=full(
                                n_period,
                                frequency_,
                                dtype="int"
                            ),
                    recency=full(
                                n_period,
                                recency_,
                                dtype="int"
                            ),
                    T=(arange(recency_-1, T_+n_period_+1)).astype("int"),
                ))
    df_.columns = [
        RawFeatures.CUSTOMER_ID,
        RawFeatures.frequency,
        RawFeatures.recency,
        RawFeatures.T
    ]
    return T_, df_


def get_customer_whatif_data(
        data_summary: DataFrame,
        customer_id: Union[int, float, str],
        n_period: int,
        T_future_transac: int) -> Tuple[int, DataFrame]:
    assert T_future_transac <= n_period, "Future \
        transaction must be before the end of future window"
    T_, history_ = get_customer_history_data(
                    data_summary,
                    customer_id,
                    n_period
                )
    new_transac_time = history_[
        history_["T"] == T_
        ].index.values[0] + T_future_transac
    history_[RawFeatures.frequency].iloc[new_transac_time:] += 1
    history_[RawFeatures.recency].iloc[new_transac_time:] = history_[
        RawFeatures.T].iloc[new_transac_time] - 0.01
    return T_, history_
