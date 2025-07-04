import pandas as pd, numpy as np, pytest, yfinance as yf
from backtest.policy_runner import run_policy

# 合成データでコアロジックを検証
def test_policy_length_match():
    price = pd.Series(np.cumsum(np.random.normal(size=400)) + 100)
    out = run_policy(price, window=50)
    assert len(out) == len(price) - 50
    assert out["equity"].min() > 0  # 全期間資産 > 0 

# 実データで回帰テスト（短期 window=20）
def test_policy_with_real_data():
    price = yf.download("AAPL", start="2020-01-01", interval="1d")["Close"]
    window = 20
    if len(price) <= window:
        pytest.skip("Insufficient price data from yfinance")
    out = run_policy(price, window=window)
    assert not out.empty and out["equity"].min() > 0 