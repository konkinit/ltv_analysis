from pandas import DataFrame
from lifetimes import BetaGeoFitter


class BetaGeoModel(BetaGeoFitter):
    def __init__(
            self,
            data: DataFrame,
            T_prediction: int) -> None:
        assert {
            'frequency',
            'recency',
            'T'} <= set(data.columns.tolist())
        super().__init__()
        self.data = data

    def fit_(self) -> None:
        self.fit(
            self.data['frequency'],
            self.data['recency'],
            self.data['T']
        )

    def plot_(self) -> None:
        pass
