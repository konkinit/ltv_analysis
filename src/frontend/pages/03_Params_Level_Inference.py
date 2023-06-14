import os
import sys
import streamlit as st

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.models import _BetaGeoModel


st.title("Customer LifeTime Value Modeling")


st.markdown(
    """
    ## Theoretical formulation

    ### Model assumptions and parameters
    The `BG/NBD` model is based on the following five assumptions:
    - While active, the number of transactions made by a customer \
    follows a Poisson process with transaction rate $\lambda$ ;
    - Heterogeneity in $\lambda$ follows a gamma distribution ;
    - After any transaction, a customer becomes inactive with \
    probability $p$ ;
    - Heterogeneity in $p$ follows a beta distribution ;
    - The transaction rate $\lambda$ and the dropout probability $p$ vary \
    independently across customers ;
    """
)


st.markdown(
    """
    ### Parameters Inference and Interpretation

    After simulation , 
    """
)

rfm_data = st.session_state["rfm_data"]
study_freq = st.session_state["study_freq"]
metadata_stats = st.session_state["metadata_stats"]

betageo_model = _BetaGeoModel(rfm_data, study_freq, metadata_stats)
betageo_model.fit()
df_betageo_model_params = betageo_model._fit_summary()

st.dataframe(
    data=df_betageo_model_params.iloc[:, :5],
    use_container_width=True
)

st.plotly_chart(
    betageo_model._global_plots()
)

st.session_state["betageo_model"] = betageo_model
