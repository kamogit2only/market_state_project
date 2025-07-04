"""
歩み窓：train=3年, test=1年
例：2015-2017学習→2018テスト, 2016-18→2019 … 2021-23→2024
"""


import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from backtest.runner import backtest
from metrics import calc_metrics
from policy.selector import select_strategy

GRID_BEST = dict(hurst_thr=0.55, vr_p_thr=0.01, mom_lb=20, mr_z=1.0)

price = yf.download("^N225", start="2014-01-01", end="2024-12-31")["Close"]
res = []

for start_year in range(2015, 2022):
    train = price[f"{start_year}-01-01" :f"{start_year+2}-12-31"]
    test = price[f"{start_year+3}-01-01" :f"{start_year+3}-12-31"]

    def run(p):  # helper
        eq, idx = [], []
        for i in range(200, len(p)):
            sub = p.iloc[: i + 1]
            sig = select_strategy(sub, **GRID_BEST).generate_signals()
            eq.append(backtest(sub, sig)["equity"].iloc[-1])
            idx.append(p.index[i])
        return pd.Series(eq, index=idx)

    m = calc_metrics(run(test))
    m["year"] = start_year + 3
    res.append(m)

df = pd.DataFrame(res)
df.to_csv("reports/rolling_oos_stats.csv", index=False)
plt.figure()
df["sharpe"].plot(kind="box")
plt.title("Rolling OOS Sharpe")
plt.savefig("reports/rolling_oos_box.png")
print(df)
