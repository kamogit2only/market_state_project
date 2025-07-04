import numpy as np
import pandas as pd

from indicators.randomness import variance_ratio


def test_vr_random_series():
    np.random.seed(42)
    price = pd.Series(np.cumsum(np.random.normal(size=2000)) + 100)
    vr, p = variance_ratio(price, lag=5)
    assert 0.7 < vr < 1.3 and p > 0.01
