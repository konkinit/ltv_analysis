import os
import sys
import streamlit as st
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.data import getDataset, Statistics, ProcessData
from src.config import RawFeatures, DataProcessingFeatures


st.title("Metadata Statistics")

df_transaction = getDataset()
metadata_stats = Statistics(df_transaction).metadata_stats()

st.markdown(
    "The following metrics and table describe the transaction \
    dataset"
)

colCust, colTransac = st.columns(2)
colCust.metric("# of Distinct customers", f"\
    {metadata_stats.n_distinct_customers}")
colTransac.metric("# of Transactions", f"\
    {metadata_stats.n_transactions}")

colFTransac, colLTransac = st.columns(2)
colFTransac.metric(
    "First Transaction Date",
    f"{metadata_stats.first_transac_date}"
)
colLTransac.metric(
    "Last Transaction Date",
    f"{metadata_stats.last_transac_date}"
)

st.dataframe(data=df_transaction.head(), use_container_width=True)

st.markdown(
    " To pursue the analysis , two features are mandantory : \n\
    - `study_frequency`: \n\
    - `calibration_period_end`: "
)

study_freq = st.selectbox(
    "Choose a frequency to compute the RFM features",
    ('D', 'W', 'M'),
    help="D stands for Day, W for Week and M for Month"
)

calibration_end_dt = st.text_input(
    'Choose a date marking the calibaration end',
    placeholder="2011-06-30",
    max_chars=10,
    help="The entered date must be in type YYYY-MM-DD"
)


rfm_data = ProcessData(
    DataProcessingFeatures(
        df_transaction.copy(),
        study_freq,
        calibration_end_dt
    )
).model_data()
rfm_data_stats = Statistics(rfm_data).rfm_data_stats()

st.markdown(
    f"After processing raw dataset and using the `lifetimes` package, \
    we extract the following RFM data. {rfm_data_stats[0]} customers data \
    are eligible for remaining analysis.\
    Below statistics about RFM features \n"
)

colF, colR, colT, colM = st.columns(4)

colR.metric("Recency", f"\
    {rfm_data[RawFeatures().recency].mean().round(2)}")
colF.metric("Frequency", f"\
    {rfm_data[RawFeatures().frequency].mean().round(2)}")
colM.metric("Monetary", f"\
    {rfm_data[RawFeatures().monetary].mean().round(2)}")
colT.metric(
    "Age",
    f"{rfm_data[RawFeatures().T].mean().round(2)} \
        {study_freq}"
)
st.dataframe(
    data=rfm_data.head(),
    use_container_width=True
)


st.session_state["rfm_data"] = rfm_data
st.session_state["study_freq"] = study_freq
st.session_state["calibration_end_dt"] = calibration_end_dt
