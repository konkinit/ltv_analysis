import os
import sys
from numpy import arange, meshgrid
from pandas import DataFrame
from plotly.express import imshow
from plotly.graph_objects import Figure
from pymc_marketing.clv import (
    BetaGeoModel,
)
from pymc import HalfNormal
from typing import Any, Tuple, List, Union

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import RawFeatures, AlivePlot_Params, Metadata_Features
from src.utils import (
    get_customer_history_data,
    get_customer_whatif_data,
    _plot_probability_alive
)


class BetaGeoModel(BetaGeoModel):
    def __init__(
            self,
            data: DataFrame,
            freq: str,
            metadata_stats: Metadata_Features
    ) -> None:
        self.data = data.copy()
        self.freq = freq
        self.metadata_stats = metadata_stats
        super().__init__(
            customer_id=self.data.index,
            frequency=self.data[RawFeatures.frequency],
            recency=self.data[RawFeatures.recency],
            T=self.data[RawFeatures.T],
            a_prior=HalfNormal.dist(10),
            b_prior=HalfNormal.dist(10),
            alpha_prior=HalfNormal.dist(10),
            r_prior=HalfNormal.dist(10)
        )

    def fit_or_load_model(self):
        pass

    def _fit_summary(self):
        return self.fit_summary().reset_index(
            drop=False).rename(columns={"index": "parameter"})

    def probability_alive_xarray(
        self, T_: int, customer_history: DataFrame
    ) -> Tuple[float, float, Any]:
        return self.expected_probability_alive(
            customer_id=customer_history[RawFeatures.CUSTOMER_ID],
            frequency=customer_history[RawFeatures.frequency],
            recency=customer_history[RawFeatures.recency],
            T=customer_history[RawFeatures.T],
        )

    def probability_alive_features(
        self, T_: int, customer_history: DataFrame
    ) -> Tuple[float, float]:
        p_alive_xarray = self.probability_alive_xarray(T_, customer_history)
        min_p_alive_ = p_alive_xarray.to_numpy().min(axis=0).min(axis=0)
        max_p_alive_ = p_alive_xarray.to_numpy().max(axis=0).max(axis=0)
        return (min_p_alive_, max_p_alive_)

    def probability_alive_study_instant(
        self, T_: int, customer_history: DataFrame
    ) -> float:
        return (
            self.probability_alive_xarray(T_, customer_history)
            .median(("draw", "chain"))
            .to_numpy()[
                customer_history[
                    customer_history[RawFeatures.T] == T_
                ].index.values[0]
            ]
        )

    def plot_probability_alive(
        self,
        customer_id: Union[float, int, str],
        n_period: int,
        fig_dim: List[int],
        *args
    ) -> None:
        T_, customer_history = (
            get_customer_whatif_data(
                self.data, self.metadata_stats, self.freq,
                customer_id, n_period, args[0]
            )
            if args
            else get_customer_history_data(
                self.data, self.metadata_stats, self.freq,
                customer_id,  n_period
            )
        )
        alive_p_study_time = self.probability_alive_study_instant(
            T_, customer_history
        )
        p_alive_xarray = self.probability_alive_xarray(T_, customer_history)
        (min_p_alive_, max_p_alive_) = self.probability_alive_features(
            T_, customer_history
        )
        status_study_time_color = (
            "green"
            if alive_p_study_time > 0.7
            else "yellow"
            if alive_p_study_time > 0.4
            else "red"
        )
        if args:
            idx_next_transac = n_period - args[0] + 1
            plot_params = AlivePlot_Params(
                customer_id, customer_history, T_, p_alive_xarray,
                status_study_time_color, idx_next_transac, max_p_alive_,
                min_p_alive_, fig_dim
            )
            _plot_probability_alive(plot_params, self.metadata_stats, args[0])
        else:
            plot_params = AlivePlot_Params(
                customer_id, customer_history, T_, p_alive_xarray,
                status_study_time_color, 0, max_p_alive_,
                min_p_alive_, fig_dim
            )
            _plot_probability_alive(plot_params, self.metadata_stats)

    def _global_plots(
        self,
        max_frequency=None,
        max_recency=None,
        title="Probability Customer is Alive",
        xlabel="Customer's Historical Frequency",
        ylabel="Customer's Recency",
        **kwargs
    ) -> Figure:
        if max_frequency is None:
            max_frequency = int(self.frequency.max())
        if max_recency is None:
            max_recency = int(self.recency.max())
        frequency = arange(max_frequency + 1)
        recency = arange(max_recency + 1)
        mesh_frequency, mesh_recency = meshgrid(frequency, recency)
        Z = (
            self.expected_probability_alive(
                customer_id=arange(mesh_recency.size),
                frequency=mesh_frequency.ravel(),
                recency=mesh_recency.ravel(),
                T=max_recency,
            )
            .mean(("draw", "chain"))
            .values.reshape(mesh_recency.shape)
        )
        fig = imshow(
            Z,
            labels={
                "color": "probability",
                "x": RawFeatures.frequency,
                "y": RawFeatures.recency
            },
            width=600, height=700,
        )
        fig.update_layout(
            xaxis_title=xlabel, yaxis_title=ylabel, title=title, autosize=True
        )
        return fig
