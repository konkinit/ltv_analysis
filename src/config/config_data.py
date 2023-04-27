from dataclasses import dataclass
from typing import Union
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
class RFM:
    max_recency: Union[int, float] = 0.0
    max_T: Union[int, float] = 0.0
    date_last_purchase: date = date.today()
