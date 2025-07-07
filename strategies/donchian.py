import pandas as pd

from strategies.base import BaseStrategy


class DonchianStrategy(BaseStrategy):
    def __init__(
        self,
        price: pd.Series,
        window: int = 55,
        vol_scale: bool = False,
        atr_window: int = 14,
        k: float = 1.0,
    ):
        super().__init__(price)
        if vol_scale:
            atr = price.diff().abs().rolling(atr_window).mean()
            adj = int((k * (atr / price).mean() * 100).round())
            window = max(20, window - adj)
        self.window = window

    def generate_signals(self) -> pd.Series:
        high = self.price.rolling(self.window).max()
        return (self.price > high.shift()).astype(int).fillna(0)
