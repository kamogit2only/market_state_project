import pandas as pd

from strategies.base import BaseStrategy


class HoldStrategy(BaseStrategy):
    def generate_signals(self) -> pd.Series:
        return pd.Series(1, index=self.price.index)
