import pandas as pd, numpy as np
from indicators.randomness import detect_regime

def test_detect_regime_runs():
    price = pd.Series(np.cumsum(np.random.normal(size=500))+100)
    res = detect_regime(price)
    assert set(res.keys()) >= {"trend","mean_revert","random"} 