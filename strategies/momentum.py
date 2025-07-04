import pandas as pd
from strategies.base import BaseStrategy
class MomentumStrategy(BaseStrategy):
    def __init__(self, price: pd.Series, lookback: int = 20):
        super().__init__(price)
        self.lookback = lookback
    def generate_signals(self) -> pd.Series:
        roc = self.price.pct_change(self.lookback)
        return (roc > 0).astype(int).reindex(self.price.index).fillna(0) 