import yfinance as yf, pandas as pd
from strategies.hold import HoldStrategy
from backtest.runner import backtest
from backtest.policy_runner import run_policy
from metrics import calc_metrics

symbol = "^N225"
price = yf.download(symbol, start="2015-01-01", end="2024-12-31")["Close"]

# Buy & Hold
bh_sig = HoldStrategy(price).generate_signals()
bh_eq = backtest(price, bh_sig)["equity"]
bh_metrics = calc_metrics(bh_eq)

# Policy
policy_eq = run_policy(price, window=100)["equity"]
policy_metrics = calc_metrics(policy_eq)

df = pd.DataFrame([bh_metrics, policy_metrics], index=["Buy&Hold", "Policy"])
df.to_csv("evaluation.csv")
print(df) 