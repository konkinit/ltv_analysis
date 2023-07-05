import streamlit as st


st.markdown(
    """
    # Customer LifeTime Value Modeling in a Non-Contractual Setting

    ## About the app

    The followwing app provides an estimation of features \
    around Customer LifeTime Value using Fader et al.'S approach. \
    For more information on the theory consult \
    [the official \
    paper](http://brucehardie.com/papers/018/fader_et_al_mksc_05.pdf)


    ## Fader et al.'s approach overview

    >Today's managers are very interested in predicting the future purchasing\
     patterns of their customers, which can then serve as an input into \
    “lifetime value” calculations. Among the models that provide such \
    capabilities, the Pareto/NBD “counting your customers” framework proposed \
    by Schmittlein et al. (1987) is highly regarded. However, despite the \
    respect it has earned, it has proven to be a difficult model to \
    implement, particularly because of computational challenges associated \
    with parameter estimation. We develop a new model, the beta-geometric/NBD \
    (BG/NBD), which represents \
    a slight variation in the behavioral “story” associated with the \
    Pareto/NBD but is vastly easier to implement. We show, for instance, \
    how its parameters can be obtained quite easily in Microsoft Excel. The \
    two models yield very similar results in a wide variety of purchasing \
    environments, leading us to suggest that the BG/NBD could be viewed as an \
    attractive alternative to the Pareto/NBD in most applications.


    ## Key Concepts

    The following concepts are mainly used in :
    - `Recency`:  represents the age of the customer when they made their \
    most recent purchases. This is equal to the duration between a \
    customer's first purchase and their latest purchase ;
    - `Frequency`: it's the count of time periods the customer had a \
    purchase in ;
    - `Monetary`: represents the average value of a given customer's \
    purchases. This is equal to the sum of all a customer`s purchases \
    divided by the total number of purchases. Note that the denominator here \
    is different than the frequency described above ;
    - `T`: represents the age of the customer in whatever time units chosen \
    (weekly, in the above dataset). This is equal to the duration between a \
    ustomer's first purchase and the end of the period under study ;
    """
)
