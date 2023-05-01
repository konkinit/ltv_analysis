import os
import sys
import streamlit as st
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.data import (
    getDataset,
)


st.title("Metadata Statistics")

df_transaction = getDataset()

st.dataframe(
    data=df_transaction.head(),
    use_container_width=True
)
