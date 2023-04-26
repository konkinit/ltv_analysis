import os
import sys
import arviz as az
import matplotlib.pyplot as plt
from pandas import DataFrame
from pymc_marketing.clv import BetaGeoModel
from pymc import HalfNormal
from typing import Any
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import (
    RawFeatures
)


class BetaGeoModel(BetaGeoModel):
    def __init__(
            self,
            data: DataFrame,
            T_prediction: int) -> None:
        self.data = data.copy()
        super().__init__(
            customer_id=self.data.index,
            frequency=self.data["frequency"],
            recency=self.data["recency"],
            T=self.data["T"],
            a_prior=HalfNormal.dist(10),
            b_prior=HalfNormal.dist(10),
            alpha_prior=HalfNormal.dist(10),
            r_prior=HalfNormal.dist(10),
        )

    def probability_alive(
            self,
            customer_history: DataFrame) -> Any:
        self.expected_probability_alive(
            customer_id=customer_history[RawFeatures.CUSTOMER_ID],
            frequency=customer_history[RawFeatures.frequency],
            recency=customer_history[RawFeatures.recency],
            T=customer_history[RawFeatures.T]
        )

    def alive_plot(self, customer_id) -> None:
        customer_history = customer_history_data(customer_id)
        p_alive = self.probability_alive(customer_history)
        az.plot_hdi(
                customer_history["T"],
                p_alive,
                color="C0"
            )
        plt.plot(
            customer_history["T"],
            p_alive.mean(("draw", "chain")),
            marker="o"
            )
        plt.axvline(
            customer_history["recency"].iloc[0],
            c="black",
            ls="--",
            label="Purchase"
            )
        plt.title(f"Probability Customer {customer_id} will purchase again")
        plt.xlabel("T")
        plt.ylabel("p")
        plt.legend()
        plt.show()

    def global_plots_(self):
        pass
