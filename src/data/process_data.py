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
from src.data import RawFeatures


class ProcessData:
    def __init__(self, data):
        self.data = data.copy()

    def processing_stack(self) -> DataFrame:
        self.data[
            RawFeatures.TRANSACTION_DATE
            ] = to_datetime(
                    self.data[RawFeatures.TRANSACTION_DATE],
                    format='mixed'
                ).dt.date
        self.data.dropna(
            axis=0,
            subset=[RawFeatures.CUSTOMER_ID],
            inplace=True
        )
        self.data = self.data[(self.data[RawFeatures.QTY] > 0)]
        self.data[RawFeatures.TOTAL_PRICE] = (self.data[RawFeatures.QTY] *
                                              self.data[RawFeatures.PRICE])
        self.data = summary_data_from_transaction_data(
                        self.data[[
                            RawFeatures.CUSTOMER_ID,
                            RawFeatures.TRANSACTION_DATE,
                            RawFeatures.TOTAL_PRICE]],
                        customer_id_col=RawFeatures.CUSTOMER_ID,
                        datetime_col=RawFeatures.TRANSACTION_DATE,
                        monetary_value_col=RawFeatures.TOTAL_PRICE,
                        freq='D'
                    )
        return self.data[self.data['frequency'] > 0]
