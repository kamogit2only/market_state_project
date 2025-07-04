import pandas as pd, numpy as np
from backtest.policy_runner import run_policy
def test_policy_runs():
    price = pd.Series(np.cumsum(np.random.normal(size=300))+100)
    out = run_policy(price, window=50)
    assert not out.empty 