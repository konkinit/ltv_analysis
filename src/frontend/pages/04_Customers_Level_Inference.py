import os
import sys
import streamlit as st

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import (
    get_customer_history_data, get_customer_whatif_data
)


st.markdown(
    r"""
    # Inference on Customer Level
    """
)


betageo_model = st.session_state["betageo_model"]
list_cohort_customers = st.session_state["list_cohort_customers"]


customer_id = st.selectbox(
    'For more insights on a customer, choose his ID',
    list_cohort_customers
)
n_period = st.number_input(
    "Enter the number of period in the future for prediction",
    min_value=1
)
time_future_transac = st.number_input(
    "Enter the number of period in the future after which the customer\
    realises a transaction",
    value=None,
    help="If a what-if scenario is not desired, let the value to `None`"
)


if time_future_transac:
    assert time_future_transac <= n_period


T_, customer_history = (
    get_customer_whatif_data(
        betageo_model.data, betageo_model.metadata_stats,
        betageo_model.freq,
        customer_id, n_period, time_future_transac
    )
    if time_future_transac
    else get_customer_history_data(
        betageo_model.data, betageo_model.metadata_stats,
        betageo_model.freq,
        customer_id,  n_period
    )
)
p_alive_now = betageo_model.probability_alive_study_instant(
    T_, customer_history
)
fig = betageo_model.plot_probability_alive(
    customer_id,
    n_period,
    time_future_transac
)
st.plotly_chart(
    fig
)
