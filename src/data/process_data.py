import os
import sys
from pandas import (
    to_datetime,
    DataFrame
)
from lifetimes.utils import (
    summary_data_from_transaction_data
)
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import (
    RawFeatures,
    RFM
)


class ProcessData:
    def __init__(
            self,
            data: DataFrame,
            freq: str,
            calibration_period_end: str):
        self.data = data.copy()
        self.freq = freq
        self.calibration_period_end = calibration_period_end

    def model_data(self) -> DataFrame:
        self.data[
            RawFeatures.TRANSACTION_DATE
            ] = to_datetime(
                    self.data[RawFeatures.TRANSACTION_DATE]
                ).dt.date
        self.data.dropna(
            axis=0,
            subset=[RawFeatures.CUSTOMER_ID],
            inplace=True
        )
        self.data = self.data[(self.data[RawFeatures.QTY] > 0)]
        self.data[RawFeatures.TOTAL_PRICE] = (self.data[RawFeatures.QTY] *
                                              self.data[RawFeatures.PRICE])
        df_ = summary_data_from_transaction_data(
                    self.data[[
                        RawFeatures.CUSTOMER_ID,
                        RawFeatures.TRANSACTION_DATE,
                        RawFeatures.TOTAL_PRICE]],
                    customer_id_col=RawFeatures.CUSTOMER_ID,
                    datetime_col=RawFeatures.TRANSACTION_DATE,
                    monetary_value_col=RawFeatures.TOTAL_PRICE,
                    freq=self.freq
                )
        RFM.max_T = df_[RawFeatures.T].max()
        RFM.max_recency = df_[RawFeatures.recency].max()
        return df_[df_[RawFeatures.frequency] > 0]
