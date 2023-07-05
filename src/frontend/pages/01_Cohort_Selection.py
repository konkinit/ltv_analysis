import streamlit as st
from datetime import date
from math import ceil


dict_cohort = {
    **{
        _year: ["Q1", "Q2", "Q3", "Q4"] for _year in range(
            2018, date.today().year
        )
    },
    date.today().year: [
        f"Q{i}" for i in range(1, 1+ceil((date.today().month)/3))
    ]
}


st.markdown(
    """
    # Cohort Setting Up

    Fader et al. discussed the conditions of impementation \
    of a `BG/NBD` model. They suggested an separated application \
    of the model based  on customer cohorts defined by the time \
    (e.g., quarter) of acquisition, acquisition channel, etc...

    Choose the cohort on which study has to be carried out
    """
)
year = st.number_input(
    'Insert a year of adhesion',
    min_value=2018,
    max_value=date.today().year
)

quarter = st.selectbox(
    'Select the quarter of adhesion',
    dict_cohort[year]
)


st.session_state["year_adhesion"] = year
st.session_state["quarter_adhesion"] = quarter
