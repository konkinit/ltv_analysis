import os
import sys
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
    get_customer_whatif_data,
    plot_
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
            ) -> Tuple[float, float, Any]:
        p_alive_xarray = self.expected_probability_alive(
            customer_id=customer_history[RawFeatures.CUSTOMER_ID],
            frequency=customer_history[RawFeatures.frequency],
            recency=customer_history[RawFeatures.recency],
            T=customer_history[RawFeatures.T]
        )
        min_p_alive_ = p_alive_xarray.to_numpy().min(axis=0).min(axis=0)
        max_p_alive_ = p_alive_xarray.to_numpy().max(axis=0).max(axis=0)
        return (
            min_p_alive_,
            max_p_alive_,
            p_alive_xarray
        )

    def alive_proba_study_time(
            self,
            T_: int,
            customer_history: DataFrame
            ) -> float:
        return self.expected_probability_alive(
                    customer_id=customer_history[RawFeatures.CUSTOMER_ID],
                    frequency=customer_history[RawFeatures.frequency],
                    recency=customer_history[RawFeatures.recency],
                    T=customer_history[RawFeatures.T]
                ).median(
                        ("draw", "chain")
                    ).to_numpy()[
                                customer_history[
                                    customer_history["T"] == T_
                                ].index.values[0]
                            ]

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
        alive_p_study_time = self.alive_proba_study_time(
                                T_,
                                customer_history
                            )
        status_study_time_color = "green" if alive_p_study_time > 0.7 else \
            "yellow" if alive_p_study_time > 0.4 else "red"
        (
            min_p_alive_,
            max_p_alive_,
            p_alive_xarray
        ) = self.probability_alive_features(
                T_,
                customer_history
            )
        plot_(
            customer_id,
            customer_history,
            T_,
            p_alive_xarray,
            status_study_time_color,
            max_p_alive_,
            min_p_alive_,
            fig_dim,
            args
        )

    def global_plots_(self):
        """
        clv.plot_probability_alive_matrix(bgm)
        plt.show()
        """
        pass
