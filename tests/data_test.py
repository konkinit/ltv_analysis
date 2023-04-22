import sys
import os
from pandas import DataFrame
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.data import (
    getDataset
)


def test_getDaaset():
    assert type(getDataset()) == DataFrame
