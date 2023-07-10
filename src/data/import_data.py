import os
import sys
from pandas import DataFrame

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import import_from_local, import_from_S3
from src.config import RawFeatures, S3Features
from src.utils import datetime_formatting


list_cols = [
    RawFeatures.CUSTOMER_ID,
    RawFeatures.TRANSACTION_DATE,
    RawFeatures.PRICE,
    RawFeatures.QTY,
]


def getDataset(*args) -> DataFrame:
    """Get raw transactional dataset

    Returns:
        DataFrame: transactional dataframe
    """
    params = S3Features()
    if os.path.isfile(os.path.join(params.local_path)):
        return datetime_formatting(
            import_from_local(params.local_path)[
                list_cols
            ]
        )
    return datetime_formatting(
        import_from_S3(
            params.endpoint,
            params.bucket,
            params.path,
            params.key_id,
            params.access_key,
            params.token,
        )[list_cols]
    )
