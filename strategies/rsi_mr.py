import numpy as np
import pandas as pd

from strategies.base import BaseStrategy


class RSIMRStrategy(BaseStrategy):
    def __init__(self, price: pd.Series, window: int = 14, thresh: int = 30,
                 vol_scale: bool = False, atr_window: int = 14, m: float = 10):
        super().__init__(price)
        if vol_scale:
            atr = price.diff().abs().rolling(atr_window).mean()
            thresh += int(m * (atr / price).mean() * 100)
        self.w, self.th = window, thresh

    def _rsi(self, s):
        delta = s.diff()
        up = delta.clip(lower=0).ewm(alpha=1 / self.w).mean()
        dn = -delta.clip(upper=0).ewm(alpha=1 / self.w).mean()
        rs = up / dn.replace({0: np.nan})
        return 100 - (100 / (1 + rs))

    def generate_signals(self) -> pd.Series:
        rsi = self._rsi(self.price)
        return (rsi < self.th).astype(int).fillna(0)
