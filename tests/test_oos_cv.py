import pandas as pd, numpy as np
from metrics import calc_metrics

def test_metrics_valid():
    eq = pd.Series(np.linspace(1, 2, 100))
    m  = calc_metrics(eq)
    assert m["total_return"] > 0 and m["sharpe"] > 0 