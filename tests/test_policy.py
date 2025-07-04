import pandas as pd, numpy as np
from backtest.policy_runner import run_policy

def test_policy_length_match():
    price = pd.Series(np.cumsum(np.random.normal(size=400)) + 100)
    out = run_policy(price, window=50)
    assert len(out) == len(price) - 50
    assert out["equity"].min() > 0  # 全期間資産 > 0 