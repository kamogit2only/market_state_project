import pandas as pd

from strategies.base import BaseStrategy


class DonchianStrategy(BaseStrategy):
    def __init__(self, price: pd.Series, window: int = 55):
        super().__init__(price)
        self.window = window

    def generate_signals(self) -> pd.Series:
        high = self.price.rolling(self.window).max()
        return (self.price > high.shift()).astype(int).fillna(0)
