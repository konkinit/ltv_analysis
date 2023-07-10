import os
import sys
from dataclasses import dataclass, field
from datetime import date
from json import load
from pandas import DataFrame
from typing import Union, List, Any

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())


tokens_path = "data/tokens.json"
token_file_present = False
if os.path.isfile(os.path.join(tokens_path)):
    with open(f"./{tokens_path}") as f:
        tokens = load(f)
        token_file_present = True


@dataclass
class S3Features:
    local_path: str = "./data/online_retail_data.csv"
    endpoint: str = tokens["endpoint_url"] if token_file_present else ""
    bucket: str = tokens["bucket"] if token_file_present else ""
    path: str = tokens["path"] if token_file_present else ""
    key_id: str = tokens["key_id"] if token_file_present else ""
    access_key: str = tokens["access_key"] if token_file_present else ""
    token: str = tokens["token"] if token_file_present else ""


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
    DATE_T: str = "date_T"
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


@dataclass
class AlivePlot_Params:
    customer_id: Union[int, float, str]
    customer_history: DataFrame
    T_: int
    p_alive_xarray: Any
    status_study_time_color: str
    idx_next_transac: int
    max_p_alive_: List[float]
    min_p_alive_: List[float]
    fig_dim: List[int]
