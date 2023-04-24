from pandas import DataFrame
from lifetimes import BetaGeoFitter


class BetaGeoModel(BetaGeoFitter):
    def __init__(
            self,
            data: DataFrame,
            T_prediction: int,
            penalizer_coef_: float = 0.0) -> None:
        """assert (
            {
                'frequency',
                'recency',
                'T'
            } <= set(data.columns.tolist()) |
            {
                'frequency_cal',
                'recency',
                'T'
            } <= set(data.columns.tolist())
            )
        """
        super().__init__(
            penalizer_coef=penalizer_coef_
        )
        self.data = data

    def fit_(self) -> None:
        self.fit(
            self.data['frequency'],
            self.data['recency'],
            self.data['T']
        )

    def fit_validation(self) -> None:
        self.fit(
            self.data['frequency_cal'],
            self.data['recency_cal'],
            self.data['T_cal']
        )

    def plot_(self) -> None:
        pass

    def probability_alive_(self):
        pass
