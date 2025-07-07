import numpy as np
import pandas as pd

from strategies.rsi_mr import RSIMRStrategy


def test_rsi_len_match():
    p = pd.Series(np.random.rand(200) + 100)
    sig = RSIMRStrategy(p).generate_signals()
    assert len(sig) == len(p) and sig.isin([0, 1]).all()
