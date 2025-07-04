import pandas as pd, numpy as np
from policy.selector_mix import select_mixed

def test_mix_runs():
    p = pd.Series(np.cumsum(np.random.normal(size=400))+100)
    strat = select_mixed(p)
    sig   = strat.generate_signals()
    assert len(sig)==len(p) and sig.isin([0,1]).all() 