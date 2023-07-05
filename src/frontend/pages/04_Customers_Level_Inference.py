import os
import sys
import streamlit as st

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import get_customer_last_transac_to_future_data


st.markdown(
    r"""
    # Inference on Customer Level

    This poage is designed to highlight customers' metrics obtained
    from modeling.
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


T_, customer_history = get_customer_last_transac_to_future_data(
    betageo_model.data, betageo_model.metadata_stats,
    betageo_model.freq,
    customer_id, n_period, time_future_transac
)
p_alive_now = betageo_model.probability_alive_study_instant(
    T_, customer_history
)

fig = betageo_model.plot_probability_alive(
    float(customer_id),
    n_period,
    time_future_transac
)
st.plotly_chart(
    fig
)
