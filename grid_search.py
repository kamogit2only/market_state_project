import itertools

import pandas as pd
import yfinance as yf

from backtest.runner import backtest
from indicators.randomness import detect_regime
from metrics import calc_metrics
from strategies.hold import HoldStrategy
from strategies.mean_revert import MeanRevertStrategy
from strategies.momentum import MomentumStrategy

# ---------------- パラメータグリッド（軽量化版） ---------------- #
grid = {
    "hurst_thr": [0.55, 0.60],
    "vr_p": [0.05],
    "mom_lb": [20, 40],
    "mr_z": [1.0, 1.5],
}
combos = list(itertools.product(*grid.values()))

# ---------------- データ取得 ---------------- #
price = yf.download("^N225", start="2015-01-01", end="2024-12-31")["Close"]


def select_strategy(sub_price, hurst_thr, vr_p, mom_lb, mr_z):
    m = detect_regime(sub_price)["metrics"]
    if m["hurst"] > hurst_thr and m["vr_p"] < vr_p:
        return MomentumStrategy(sub_price, lookback=mom_lb)
    if m["hurst"] < (1 - hurst_thr) and m["vr_p"] < vr_p:
        return MeanRevertStrategy(sub_price, z=mr_z)
    return HoldStrategy(sub_price)


def run_once(hurst_thr, vr_p, mom_lb, mr_z):
    equity = []
    idx = []
    for i in range(100, len(price)):  # windowを100に短縮
        sub = price.iloc[: i + 1]
        strat = select_strategy(sub, hurst_thr, vr_p, mom_lb, mr_z)
        sig = strat.generate_signals()
        bt = backtest(sub, sig)
        equity.append(bt["equity"].iloc[-1])
        idx.append(price.index[i])
    return calc_metrics(pd.Series(equity, index=idx))


records = []
for c in combos:
    print(f"Processing combo: {c}")
    m = run_once(*c)
    records.append({**dict(zip(grid.keys(), c)), **m})

df = pd.DataFrame(records)
df.to_csv("grid_results.csv", index=False)
print(df.sort_values("sharpe", ascending=False).head(10))
