import os
import sys
import json
from dataclasses import dataclass
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import (
    import_from_local,
    import_from_S3
)
from src.config import RawFeatures
from src.utils import datetime_formatting


with open("./data/tokens.json") as f:
    tokens = json.load(f)


@dataclass
class ImportData:
    local_path: str = "./data/online_retail_data.csv"
    endpoint: str = tokens["endpoint_url"]
    bucket: str = tokens["bucket"]
    path: str = tokens["path"]
    key_id: str = tokens["key_id"]
    access_key: str = tokens["access_key"]
    token: str = tokens["token"]


def getDataset():
    params = ImportData()
    if os.path.isfile(os.path.join(params.local_path)):
        return datetime_formatting(
            import_from_local(
                params.local_path
            )[[
                RawFeatures.CUSTOMER_ID,
                RawFeatures.TRANSACTION_DATE,
                RawFeatures.PRICE,
                RawFeatures.QTY
            ]]
        )
    return datetime_formatting(
        import_from_S3(
            params.endpoint,
            params.bucket,
            params.path,
            params.key_id,
            params.access_key,
            params.token
        )[[
            RawFeatures.CUSTOMER_ID,
            RawFeatures.TRANSACTION_DATE,
            RawFeatures.PRICE,
            RawFeatures.QTY
        ]]
    )
