import numpy as np
import pandas as pd

from strategies.bband_mr import BBandMRStrategy


def test_bband_len_match():
    p = pd.Series(np.random.rand(200) + 100)
    sig = BBandMRStrategy(p).generate_signals()
    assert len(sig) == len(p) and set(sig.unique()) <= {0, 1}
