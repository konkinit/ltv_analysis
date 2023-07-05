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
    get_customer_last_transac_to_future_data,
    _plot_probability_alive
)


class _BetaGeoModel(BetaGeoModel):
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

    def _fit_summary(self) -> DataFrame:
        """Fit and summarize the model

        Returns:
            Dataframe: parameters inference table
        """
        return self.fit_summary().reset_index(drop=False).rename(
            columns={"index": "parameter"}
        )

    def probability_alive_xarray(
        self, T_: int, customer_history: DataFrame
    ) -> Tuple[float, float, Any]:
        """Derive the alive probabilities during customer lifetime

        Args:
            T_ (int): customer age
            customer_history (DataFrame): customer RFM history data

        Returns:
            Tuple[float, float, Any]: _description_
        """
        return self.expected_probability_alive(
            customer_id=customer_history[RawFeatures.CUSTOMER_ID],
            frequency=customer_history[RawFeatures.frequency],
            recency=customer_history[RawFeatures.recency],
            T=customer_history[RawFeatures.T],
        )

    def probability_alive_features(
        self, T_: int, customer_history: DataFrame
    ) -> Tuple[float, float]:
        """Get customer alive probabilities bundaries

        Args:
            T_ (int): customer's age
            customer_history (DataFrame): customer's RFM history data

        Returns:
            Tuple[float, float]: min and max of customer's alive probabilities
        """
        p_alive_xarray = self.probability_alive_xarray(T_, customer_history)
        min_p_alive_ = p_alive_xarray.to_numpy().min(axis=0).min(axis=0)
        max_p_alive_ = p_alive_xarray.to_numpy().max(axis=0).max(axis=0)
        return (min_p_alive_, max_p_alive_)

    def probability_alive_study_instant(
        self, T_: int, customer_history: DataFrame
    ) -> float:
        """Get the alive probability at the study time

        Args:
            T_ (int): customer's age
            customer_history (DataFrame): customer's RFM history data

        Returns:
            float: alive probability at the moment
        """
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
        time_future_transac: int = None,
        fig_dim: List[int] = [1500, 700]
    ) -> Figure:
        """Predict customer's future behaviour and
        Plot alive probability from the last transaction to the
        a certain period in the future

        Args:
            customer_id (Union[float, int, str]): customer's id
            n_period (int): number of period in the future
            time_future_transac (int): instant of contrefactual transactoion
            in the future
            fig_dim (List[int]): plot dimensions

        Returns:
            Figure: figure object
        """
        T_, customer_history = get_customer_last_transac_to_future_data(
            self.data, self.metadata_stats, self.freq,
            customer_id, n_period, time_future_transac
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
        if time_future_transac:
            idx_next_transac = n_period - time_future_transac + 1
            plot_params = AlivePlot_Params(
                customer_id, customer_history, T_, p_alive_xarray,
                status_study_time_color, idx_next_transac, max_p_alive_,
                min_p_alive_, fig_dim
            )
            return _plot_probability_alive(
                plot_params, self.metadata_stats, time_future_transac
            )
        else:
            plot_params = AlivePlot_Params(
                customer_id, customer_history, T_, p_alive_xarray,
                status_study_time_color, 0, max_p_alive_,
                min_p_alive_, fig_dim
            )
            return _plot_probability_alive(plot_params, self.metadata_stats)

    def _global_plots(
        self,
        max_frequency=None,
        max_recency=None,
        title="Probability Customer is Alive",
        xlabel="Customer's Historical Frequency",
        ylabel="Customer's Recency",
        **kwargs
    ) -> Figure:
        """Produce recency X frequency heatmap

        Args:
            max_frequency (_type_, optional): maximum value of frequency.
            Defaults to None.
            max_recency (_type_, optional): maximum value of recency.
            Defaults to None.
            title (str, optional): figure title.
            Defaults to "Probability Customer is Alive".
            xlabel (str, optional): x axis label.
            Defaults to "Customer's Historical Frequency".
            ylabel (str, optional): y axis label.
            Defaults to "Customer's Recency".

        Returns:
            Figure: heat map figure object
        """
        if max_frequency is None:
            max_frequency = int(self.frequency.max())
        if max_recency is None:
            max_recency = int(self.recency.max())
        frequency, recency = arange(max_frequency + 1), arange(max_recency + 1)
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
