import os
import sys
from datetime import datetime, timedelta
from numpy import full, arange
from pandas import DataFrame
from typing import (
    Union,
)

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import RawFeatures, Metadata_Features


_freq_dict = {
    "D": "days",
    "W": "weeks"
}


class Customer:
    def __init__(self, customer_id: Union[float, str, int]):
        self.id = customer_id
        self.T = 0
        self.frequency = 0
        self.recency = 0
        self.alive_probability = 0.0

    def rfm_data(
            self, gloabl_rfm_data: DataFrame
    ) -> DataFrame:
        """Get customer RFM data

        Args:
            gloabl_rfm_data (DataFrame): cohort RFM data

        Returns:
            DataFrame: customer rfm data
        """
        self.T = int(gloabl_rfm_data.loc[self.id][RawFeatures.T])
        self.frequency = int(
            gloabl_rfm_data.loc[self.id][RawFeatures.frequency]
        )
        self.recency = int(gloabl_rfm_data.loc[self.id][RawFeatures.recency])
        return gloabl_rfm_data.loc[self.id]

    def rfm_data_from_last(
            self,
            gloabl_rfm_data: DataFrame,
            metadata_stats: Metadata_Features,
            freq: str,
            n_period_: int,
            T_future_transac: int = None
    ) -> DataFrame:
        """Get customer RFM history data

        Args:
            data_summary (DataFrame): RFM data
            metadata_stats (Metadata_Features): metadata statistics
            freq (str): time frequency
            customer_id (Union[int, float, str]): customer id
            n_period (int): number of freq

        Returns:
            Tuple[int, DataFrame]: a tuple composed of customer age and
            his RFM data history
        """
        _ = self.rfm_data(gloabl_rfm_data)
        n_period = int(self.T - self.recency + 2 + n_period_)
        df_ = DataFrame(
            dict(
                Customer_ID=full(n_period, self.id, dtype="int"),
                frequency=full(n_period, self.frequency, dtype="int"),
                recency=full(n_period, self.recency, dtype="int"),
                T=(arange(
                    self.recency - 1, self.T + n_period_ + 1
                )).astype("int"),
            )
        )
        df_.columns = [
            RawFeatures.CUSTOMER_ID,
            RawFeatures.frequency,
            RawFeatures.recency,
            RawFeatures.T
        ]
        if type(metadata_stats.last_transac_date) == str:
            _last_transac_date = datetime.strptime(
                metadata_stats.last_transac_date,
                "%Y-%m-%d %H:%M"
            )
        else:
            _last_transac_date = metadata_stats.last_transac_date
        df_[RawFeatures.DATE_T] = (df_[RawFeatures.T] - self.T).apply(
            lambda x: _last_transac_date + timedelta(
                **{_freq_dict[freq]: x}
            )
        )
        if T_future_transac:
            new_transac_time = df_[
                df_[RawFeatures.T] == self.T
            ].index.values[0] + T_future_transac
            df_[RawFeatures.frequency].iloc[new_transac_time:] += 1
            df_[RawFeatures.recency].iloc[new_transac_time:] = (
                df_[RawFeatures.T].iloc[new_transac_time] - 0.01
            )
            return df_
        return df_
