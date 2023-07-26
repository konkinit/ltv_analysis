import os
import sys
import streamlit as st

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.models import _BetaGeoModel


_rfm_data = __import__(
    'pages.02_MetaData_Statistics',
    fromlist=['_rfm_data']
)._rfm_data


st.title(
    """
    Customer LifeTime Value Modeling with Beta-Geo
    """
)


st.markdown(
    r"""
    ## Theoretical formulation

    ### Model assumptions and parameters
    The `BG/NBD` model is based on the following five assumptions:
    - While active, the number of transactions made by a customer
    follows a Poisson process with transaction rate $\lambda$ ;
    - Heterogeneity in $\lambda$ follows a gamma distribution ;
    - After any transaction, a customer becomes inactive with
    probability $p$ ;
    - Heterogeneity in $p$ follows a beta distribution ;
    - The transaction rate $\lambda$ and the dropout probability $p$ vary
    independently across customers ;
    """
)


st.markdown(
    """
    ### Parameters Inference and Interpretation

    After simulation ,
    """
)

rfm_data = _rfm_data()
study_freq = st.session_state["study_freq"]
metadata_stats = st.session_state["metadata_stats"]


betageo_model = _BetaGeoModel(rfm_data, study_freq, metadata_stats)
betageo_model.fit()
df_betageo_model_params = betageo_model._fit_summary()


st.session_state["betageo_model"] = betageo_model


col_a, col_b, col_alpha, col_r = st.columns(4)
col_a.metric(
    "$a$", f"{df_betageo_model_params.iloc[0, 1]}"
)
col_b.metric(
    "$b$", f"{df_betageo_model_params.iloc[1, 1]}"
)
col_alpha.metric(
    r"$\alpha$", f"{df_betageo_model_params.iloc[2, 1]}"
)
col_r.metric(
    "$r$", f"{df_betageo_model_params.iloc[3, 1]}"
)

st.plotly_chart(
    betageo_model._global_plots(),
    use_container_width=True
)
