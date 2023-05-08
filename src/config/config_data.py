from datetime import date
from dataclasses import dataclass, field
from pandas import DataFrame
from typing import Union, List


@dataclass
class RawFeatures:
    CUSTOMER_ID: str = "Customer ID"
    TRANSACTION_DATE: str = "InvoiceDate"
    PRICE: str = "Price"
    QTY: str = "Quantity"
    TOTAL_PRICE: str = "Total Price"
    frequency: str = "frequency"
    recency: str = "recency"
    T: str = "T"
    monetary: str = "monetary_value"


@dataclass
class DataProcessingFeatures:
    data: DataFrame
    study_freq: str
    calibration_period_end: str


@dataclass
class Metadata_Features:
    n_distinct_customers: int
    n_vars: int
    n_transactions: int
    first_transac_date: str
    last_transac_date: str
    df_desc_qty_price: DataFrame


@dataclass
class RFM_Features:
    max_recency: List[Union[int, float]] = field(default_factory=list)
    max_T: List[Union[int, float]] = field(default_factory=list)
    date_last_purchase: List[date] = field(default_factory=list)
