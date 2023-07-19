import os
import sys
import streamlit as st
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.data import getDataset, Statistics, ProcessData
from src.config import RawFeatures, DataProcessingFeatures


year = st.session_state["year_adhesion"]
quarter = st.session_state["quarter_adhesion"]
status = st.session_state["status"]


st.markdown(
    """
    # Metadata Statistics

    Remind on cohort characteristics
    """
)


(
    col_status,
    col_adh_year,
    col_adh_month,
) = st.columns(3)


col_adh_year.metric(
    "Adhesion Year",
    f"{year}"
)
col_adh_month.metric(
    "Adhesion Quarter",
    f"{quarter}"
)
col_status.metric(
    "Cohort Status",
    f"{status}"
)


st.markdown(
    """
    The following metrics and table describe the transaction \
    data of the cohort:
    """
)


df_transaction = getDataset(year, quarter, status)
metadata_stats = Statistics(df_transaction).metadata_stats()


st.session_state["metadata_stats"] = metadata_stats


colCust, colTransac = st.columns(2)
colCust.metric("Number of Distinct customers", f"\
    {metadata_stats.n_distinct_customers}")
colTransac.metric("Number of Transactions", f"\
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
    options=('D', 'W', 'M'),
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
st.session_state["list_cohort_customers"] = list(
    rfm_data.reset_index().iloc[:, 0].unique()
)
st.session_state["study_freq"] = study_freq
st.session_state["calibration_end_dt"] = calibration_end_dt
