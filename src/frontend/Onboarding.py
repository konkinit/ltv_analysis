import streamlit as st


st.title("Customer LifeTime Value Modeling in a Non-Contractual Setting")

st.subheader("About the app")

st.markdown(
    "The followwing app provides an estimation of features \
    around Customer LifeTime Value using Fader et al.'S approach. \
    For more information on the theory consult \
    [the official \
    paper](http://brucehardie.com/papers/018/fader_et_al_mksc_05.pdf)"
)

st.subheader("Fader et al.'s approach overview")

st.markdown("")

st.subheader("Key Concepts")

st.markdown(
    " The following concepts are mainly used in : \n\
    - `Recency`:  represents the age of the customer when they made their \
    most recent purchases. This is equal to the duration between a \
    customer's first purchase and their latest purchase \n\
    - `Frequency`: it's the count of time periods the customer had a \
    purchase in. \n\
    - `Monetary`: represents the average value of a given customer's \
    purchases. This is equal to the sum of all a customer`s purchases \
    divided by the total number of purchases. Note that the denominator here \
    is different than the frequency described above. \n\
    - `T`: represents the age of the customer in whatever time units chosen \
    (weekly, in the above dataset). This is equal to the duration between a \
    ustomer's first purchase and the end of the period under study."
)
