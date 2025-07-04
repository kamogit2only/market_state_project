import pandas as pd, numpy as np
from strategies.donchian import DonchianStrategy

def test_donchian_len_match():
    p = pd.Series(np.random.rand(200)+100)
    sig = DonchianStrategy(p).generate_signals()
    assert len(sig) == len(p) and sig.isin([0,1]).all() 