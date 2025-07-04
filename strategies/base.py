import pandas as pd
class BaseStrategy:
    """Minimal interface: feed price Series, return position Series (1 or 0)."""
    def __init__(self, price: pd.Series):
        self.price = price
    def generate_signals(self) -> pd.Series:
        raise NotImplementedError 