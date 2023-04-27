import os
import sys
import plotly.express as px
from pandas import DataFrame
from pymc_marketing.clv import BetaGeoModel
from pymc import HalfNormal
from typing import (
    Any,
    Tuple,
    List,
    Union
)
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import (
    RawFeatures
)
from src.utils import (
    get_customer_history_data,
    get_customer_whatif_data
)


class BetaGeoModel(BetaGeoModel):
    def __init__(
            self,
            data: DataFrame) -> None:
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
            T_: int,
            customer_history: DataFrame) -> Tuple[Any]:
        alive_proba_xarray = self.expected_probability_alive(
            customer_id=customer_history[RawFeatures.CUSTOMER_ID],
            frequency=customer_history[RawFeatures.frequency],
            recency=customer_history[RawFeatures.recency],
            T=customer_history[RawFeatures.T]
        )
        alive_proba_study_time = alive_proba_xarray.median(
                                    ("draw", "chain")
                                ).to_numpy()[
                                    customer_history[
                                        customer_history["T"] == T_
                                    ].index.values[0]
                                ]
        return alive_proba_study_time, alive_proba_xarray

    def plot_probability_alive(
            self,
            customer_id: Union[float, int, str],
            n_period: int,
            fig_dim: List[int],
            *args) -> None:
        T_, customer_history = get_customer_whatif_data(
                                self.data,
                                customer_id,
                                n_period,
                                args[0]
                            ) if args else get_customer_history_data(
                                                self.data,
                                                customer_id,
                                                n_period
                                            )
        _, p_alive = self.probability_alive(
            T_,
            customer_history
        )
        """az.plot_hdi(
                customer_history[RawFeatures.T],
                p_alive,
                color="C0"
        )"""
        fig = px.line(
            x=customer_history[RawFeatures.T],
            y=p_alive.median(("draw", "chain")),
            width=fig_dim[0],
            height=fig_dim[1],
            markers=True,
            line_shape='linear',
            title=f"Probability Customer {customer_id} will purchase again"
            )
        fig.update_traces(patch={"line_shape": "spline"})
        fig.add_vline(
            x=T_,
            line_width=3,
            line_dash="dash",
            line_color="red",
            annotation_text="Instant t"
        )
        fig.add_vline(
            x=customer_history[RawFeatures.recency].iloc[0],
            line_width=3,
            line_dash="dash",
            line_color="black",
            annotation_text="Purchase"
        )
        if args:
            fig.add_vline(
                x=customer_history[RawFeatures.recency].iloc[-1],
                line_width=3,
                line_dash="dash",
                line_color="black",
                annotation_text="Purchase"
            )
        fig.update_layout(
            xaxis_title="T",
            yaxis_title="probability"
        )
        fig.show()

    def global_plots_(self):
        pass
