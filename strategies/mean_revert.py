import pandas as pd
from strategies.base import BaseStrategy
class MeanRevertStrategy(BaseStrategy):
    def __init__(self, price: pd.Series, window: int = 20, z: float = 1.0):
        super().__init__(price)
        self.window, self.z = window, z
    def generate_signals(self) -> pd.Series:
        ma = self.price.rolling(self.window).mean()
        sd = self.price.rolling(self.window).std()
        zscore = (self.price - ma) / sd
        return (zscore < -self.z).astype(int).reindex(self.price.index).fillna(0) 