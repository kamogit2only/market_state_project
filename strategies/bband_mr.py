import pandas as pd
from strategies.base import BaseStrategy

class BBandMRStrategy(BaseStrategy):
    def __init__(self, price: pd.Series, window:int=20, k:float=1.0):
        super().__init__(price)
        self.window, self.k = window, k
    
    def generate_signals(self) -> pd.Series:
        ma = self.price.rolling(self.window).mean()
        sd = self.price.rolling(self.window).std()
        lower = ma - self.k * sd
        return (self.price < lower).astype(int).fillna(0) 