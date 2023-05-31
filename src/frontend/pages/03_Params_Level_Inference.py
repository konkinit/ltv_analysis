import os
import sys
import streamlit as st

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.models import BetaGeoModel


st.title("Customer LifeTime Value Modeling")


st.subheader("Theoretical formulation")


st.subheader("Parameters Inference and Interpretation")

rfm_data = st.session_state["rfm_data"]
study_freq = st.session_state["study_freq"]

betageo_model = BetaGeoModel(rfm_data, study_freq)
betageo_model.fit()
df_betageo_model_params = betageo_model._fit_summary()

st.dataframe(
    data=df_betageo_model_params,
    use_container_width=False
)

st.plotly_chart(
    betageo_model._global_plots()
)
