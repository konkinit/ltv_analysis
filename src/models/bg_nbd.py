import os
import sys
import plotly.graph_objects as go
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

    def probability_alive_features(
            self,
            T_: int,
            customer_history: DataFrame
            ) -> Tuple[float, float, float, Any]:
        p_alive_xarray = self.expected_probability_alive(
            customer_id=customer_history[RawFeatures.CUSTOMER_ID],
            frequency=customer_history[RawFeatures.frequency],
            recency=customer_history[RawFeatures.recency],
            T=customer_history[RawFeatures.T]
        )
        min_p_alive_ = p_alive_xarray.to_numpy().min(axis=0).min(axis=0)
        max_p_alive_ = p_alive_xarray.to_numpy().max(axis=0).max(axis=0)
        alive_proba_study_time = p_alive_xarray.median(
                                    ("draw", "chain")
                                ).to_numpy()[
                                    customer_history[
                                        customer_history["T"] == T_
                                    ].index.values[0]
                                ]
        return (
            alive_proba_study_time,
            min_p_alive_,
            max_p_alive_,
            p_alive_xarray
        )

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
        (
            alive_proba_study_time,
            min_p_alive_,
            max_p_alive_,
            p_alive_xarray
        ) = self.probability_alive_features(
                T_,
                customer_history
            )

        fig = go.Figure([
                go.Scatter(
                    x=customer_history[RawFeatures.T],
                    y=p_alive_xarray.median(("draw", "chain")),
                    width=4,
                    marker=True,
                ),
                go.Scatter(
                    x=list(
                        customer_history[RawFeatures.T]
                      )+list(
                            customer_history[RawFeatures.T][::-1]
                        ),
                    y=list(max_p_alive_)+list(min_p_alive_[::-1]),
                    fill='toself',
                    hoverinfo='skip',
                    showlegend=False,
                )
            ])
        fig.update_layout(
            xaxis_title="T",
            yaxis_title="probability",
            title=f"Probability Customer {customer_id} will purchase again",
            hovermode='x',
            width=fig_dim[0],
            height=fig_dim[1],
        )
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
        fig.show()

    def global_plots_(self):
        pass
