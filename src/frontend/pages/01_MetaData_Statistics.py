import os
import sys
import streamlit as st
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.data import (
    getDataset,
    Statistics,
    ProcessData
)


st.title("Metadata Statistics")

df_transaction = getDataset()
metadata_stats = Statistics(df_transaction).metadata_stats()

st.markdown(
    f"The dataset contains information on \
    `{metadata_stats.n_distinct_customers}` distinct customers explained by \
    `{metadata_stats.n_vars}` features. The dataset gathers \
    `{metadata_stats.n_transactions}` transactions the first one carries out \
    on `{metadata_stats.first_transac_date}` and the last one on \
    `{metadata_stats.last_transac_date}`. \
    Below an example of table \n"
)

st.dataframe(
    data=df_transaction.head(),
    use_container_width=False
)

data_summary = ProcessData(
                    df_transaction,
                    'D',
                    '2011-06-30'
                ).model_data()
rfm_data_stats = Statistics(data_summary).rfm_data_stats()

st.markdown(
    f"After processing raw dataset and using the `lifetimes` package, \
    we extract the following RFM data. {rfm_data_stats[0]} customers data \
    are eligible for remaining analysis.\
    Below an example of table \n"
)

st.dataframe(
    data=rfm_data_stats[1],
    use_container_width=False
)
