import os
import sys
import streamlit as st
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.data import (
    getDataset,
    Statistics,
)
from src.config import Metadata_Features


st.title("Metadata Statistics")

df_transaction = getDataset()
metadata_stats = Metadata_Features(
                    Statistics(df_transaction).metadata_stats()
                )

st.text(
    f"The dataset contains information on \
    {metadata_stats.n_distinct_customers} distincts customers explained by \
    {metadata_stats.n_vars} features. The dataset gathers \
    {metadata_stats.n_transactions} transactions the first one carries out \
    on {metadata_stats.first_transac_date} and the last one on \
    {metadata_stats.last_transac_date}. "
)

st.dataframe(
    data=df_transaction.head(),
    use_container_width=True
)
