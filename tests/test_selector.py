import numpy as np
import pandas as pd

from policy.selector import select_strategy


def test_selector_output():
    price = pd.Series(np.cumsum(np.random.normal(size=300)) + 100)
    strat = select_strategy(price, 0.55, 0.05, 20, 1.0)
    sig = strat.generate_signals()
    assert len(sig) == len(price)
