import sys
import os
from pandas import DataFrame

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import DataProcessingFeatures
from src.data import getDataset, ProcessData


def test_getDaaset():
    assert type(getDataset()) == DataFrame


def test_data_processing():
    """Assert frequency and recency order
    """
    data_inst = ProcessData(DataProcessingFeatures(
        getDataset(), "D", "2011-06-30"
        )
    )
    data_summary = data_inst.model_data()
    assert (data_summary.frequency > data_summary.recency).sum() == 0
