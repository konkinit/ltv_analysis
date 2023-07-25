import os
import sys
from datetime import datetime, timedelta
import streamlit as st
from pandas import DataFrame

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import convert_df
from src.data import Customer
from src.config import RawFeatures


year = st.session_state["year_adhesion"]
quarter = st.session_state["quarter_adhesion"]
status = st.session_state["status"]
betageo_model = st.session_state["betageo_model"]
list_cohort_customers = st.session_state["list_cohort_customers"]
last_transac_date = st.session_state["metadata_stats"].last_transac_date[:10]
freq = betageo_model.freq


st.markdown(
    r"""
    # Inference on Customer Level

    This poage is designed to highlight customers' metrics obtained
    from the model and customers' behaviours
    """
)

if "df_customer_alive_proabiliity" not in st.session_state:
    df_customer_alive_proabiliity = DataFrame(
        {
            RawFeatures.CUSTOMER_ID: list_cohort_customers,
            RawFeatures.ALIVE_PROBA: list(
                map(
                    lambda x: betageo_model.probability_alive_study_instant(
                        Customer(x)
                    ).round(4),
                    list_cohort_customers
                )
            )
        }
    )
    st.session_state[
        "df_customer_alive_proabiliity"
    ] = df_customer_alive_proabiliity
else:
    df_customer_alive_proabiliity = st.session_state[
        "df_customer_alive_proabiliity"
    ]

activity_cutoff = st.slider(
    'Choose an alive probability cutoff ', min_value=0.0, max_value=1.0,
    value=0.5, step=0.05
)

customer_id = st.selectbox(
    f"Select a customer who has an activity probability at date less \
    than {activity_cutoff}",
    df_customer_alive_proabiliity.query(
        f"{RawFeatures.ALIVE_PROBA} <= @activity_cutoff"
    )[RawFeatures.CUSTOMER_ID].tolist()
)
n_period = st.number_input(
    "Enter the number of period in the future for prediction", min_value=2
)
perform_what_if = st.checkbox("Perform a what-if analysis")
time_future_transac = st.number_input(
    "Enter the number of period in the future after which the customer\
    realises a transaction",
    value=0,
    max_value=n_period,
    label_visibility="collapsed",
    help="If a what-if scenario is not desired, let the value to `None`",
)

if not perform_what_if:
    time_future_transac = None

customer = Customer(customer_id)
fig = betageo_model.plot_probability_alive(
    customer, n_period, time_future_transac
)

(
    col_id,
    col_alive_proba,
    col_alive_proba_futur,
    col_recency,
    col_frequency,
    col_age,
    col_monetaryy,
) = st.columns(
    [
        2, 2, 2, 1, 1, 1, 2,
    ]
)
col_id.metric("Customer ID", f"{customer.id}")
col_alive_proba.metric(
    f"Alive Probability on {last_transac_date}",
    f"{customer.alive_probability.round(3)}"
)
last_transac_date_ = (
    datetime.strptime(
        last_transac_date, "%Y-%m-%d"
    ) + timedelta(n_period)
).strftime("%Y-%m-%d")
col_alive_proba_futur.metric(
    f"Alive Probability on {last_transac_date_}",
    f"{customer.alive_probability_futur.round(3)}",
    delta='{:.1%}'.format(
        -1 + customer.alive_probability_futur/customer.alive_probability
    )
)
col_recency.metric("Recency", f"{customer.recency} {freq}")
col_frequency.metric("Frequency", f"{customer.frequency}")
col_monetaryy.metric("Monetary", f"{round(customer.monetary, 2)}")
col_age.metric("Age", f"{customer.T} {freq}")

st.plotly_chart(fig, use_container_width=True)


csv = convert_df(df_customer_alive_proabiliity)
st.download_button(
    label="Download customers' alive probability as CSV",
    data=csv,
    file_name=f'customers_alive_proba_{status}_{str(year)[2:]}_{quarter}.csv',
    mime='text/csv',
)
