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

    def clean_data(self) -> None:
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

    def model_data(self) -> DataFrame:
        self.clean_data()
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
        return df_[df_[RawFeatures.frequency] > 0]
