import pandas as pd, numpy as np
from policy.selector import select_strategy
def test_selector_output():
    price = pd.Series(np.cumsum(np.random.normal(size=300))+100)
    strat = select_strategy(price, 0.55, 0.05, 20, 1.0)
    sig = strat.generate_signals()
    assert len(sig) == len(price) 