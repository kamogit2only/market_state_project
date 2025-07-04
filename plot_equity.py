import matplotlib.pyplot as plt
import yfinance as yf

from backtest.policy_runner import run_policy
from backtest.runner import backtest
from strategies.hold import HoldStrategy

symbol = "^N225"
price = yf.download(symbol, start="2015-01-01", end="2024-12-31")["Close"]

bh_eq = backtest(price, HoldStrategy(price).generate_signals())["equity"]
policy_eq = run_policy(price, window=100)["equity"]

plt.figure()
bh_eq.plot(label="Buy&Hold")
policy_eq.plot(label="Policy")
plt.title("Equity Curve")
plt.legend()
plt.savefig("equity.png")
print("equity.png saved")
