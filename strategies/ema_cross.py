import pandas as pd
from strategies.base import BaseStrategy

class EMACrossStrategy(BaseStrategy):
    def __init__(self, price: pd.Series, fast:int=20, slow:int=60):
        super().__init__(price)
        self.fast, self.slow = fast, slow
    
    def generate_signals(self) -> pd.Series:
        ema_fast = self.price.ewm(span=self.fast).mean()
        ema_slow = self.price.ewm(span=self.slow).mean()
        return (ema_fast > ema_slow).astype(int) 