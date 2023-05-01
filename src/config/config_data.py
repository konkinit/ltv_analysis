from dataclasses import dataclass, field
from typing import Union, List
from datetime import date


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


@dataclass
class Metadata_Features:
    n_distinct_customers: int


@dataclass
class RFM_Features:
    max_recency: List[Union[int, float]] = field(default_factory=list)
    max_T: List[Union[int, float]] = field(default_factory=list)
    date_last_purchase: List[date] = field(default_factory=list)
