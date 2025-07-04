import pandas as pd, numpy as np
from strategies.ema_cross import EMACrossStrategy

def test_ema_cross_len_match():
    p = pd.Series(np.random.rand(200)+100)
    sig = EMACrossStrategy(p).generate_signals()
    assert len(sig) == len(p) and set(sig.unique()) <= {0,1} 