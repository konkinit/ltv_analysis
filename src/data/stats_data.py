import os
import sys
from pandas import DataFrame
from typing import Tuple
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import (
    RawFeatures,
    Metadata_Features
)


class Statistics:
    def __init__(
            self,
            data) -> None:
        self.data = data.copy()

    def metadata_stats(
            self) -> Metadata_Features:
        n_transactions = self.data.shape[0]
        n_vars = self.data.shape[1]
        n_distinct_custumers = len(
                            self.data[RawFeatures.CUSTOMER_ID].unique()
                        )
        first_transac_date = self.data[
                                RawFeatures.TRANSACTION_DATE
                                ].dropna().sort_values().values[0]
        last_transac_date = self.data[
                                RawFeatures.TRANSACTION_DATE
                                ].dropna().sort_values().values[-1]
        df_desc_qty_price = self.data[[
                                RawFeatures.QTY,
                                RawFeatures.PRICE
                                ]].describe().iloc[[0, 1, 3, 5, 7], :]
        return Metadata_Features(
                    n_distinct_custumers,
                    n_vars,
                    n_transactions,
                    first_transac_date,
                    last_transac_date,
                    df_desc_qty_price
        )

    def rfm_data_stats(self) -> Tuple[int, DataFrame]:
        return (
            self.data.shape[0],
            self.data.describe().iloc[[0, 1, 2, 3, 5, 7], :]
        )
