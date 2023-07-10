import os
import sys
import streamlit as st

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.data import Customer


st.markdown(
    r"""
    # Inference on Customer Level

    This poage is designed to highlight customers' metrics obtained
    from modeling.
    """
)


betageo_model = st.session_state["betageo_model"]
list_cohort_customers = st.session_state["list_cohort_customers"]
freq = betageo_model.freq

customer_id = st.selectbox(
    'For more insights on a customer, choose his ID',
    list_cohort_customers
)
n_period = st.number_input(
    "Enter the number of period in the future for prediction",
    min_value=2
)
perform_what_if = st.checkbox("Perform a what-if analysis")
time_future_transac = st.number_input(
    "Enter the number of period in the future after which the customer\
    realises a transaction",
    value=0,
    max_value=n_period,
    label_visibility="collapsed",
    help="If a what-if scenario is not desired, let the value to `None`"
)

if not perform_what_if:
    time_future_transac = None

customer = Customer(customer_id)
fig = betageo_model.plot_probability_alive(
    customer,
    n_period,
    time_future_transac
)

col_id, col_alive_proba, col_recency, col_frequency, col_age = st.columns(5)
col_id.metric(
    "Customer ID", f"{customer.id}"
)
col_alive_proba.metric(
    "Alive Probability", f"{customer.alive_probability.round(3)}"
)
col_recency.metric(
    "Recency", f"{customer.recency} {freq}"
)
col_frequency.metric(
    "Frequency", f"{customer.frequency}"
)
col_age.metric(
    "Age", f"{customer.T} {freq}"
)

st.plotly_chart(
    fig
)
