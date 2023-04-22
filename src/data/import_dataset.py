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


with open("./data/tokens.json") as f:
    tokens = json.load(f)


@dataclass
class ImportData:
    local_path: str = "."
    endpoint: str = tokens["endpoint_url"]
    bucket: str = tokens["bucket"]
    path: str = tokens["path"]
    key_id: str = tokens["key_id"]
    access_key: str = tokens["access_key"]
    token: str = tokens["token"]


def getDataset():
    params = ImportData()
    try:
        return import_from_local(params.local_path)
    finally:
        return import_from_S3(
            params.endpoint,
            params.bucket,
            params.path,
            params.key_id,
            params.access_key,
            params.token
        )
