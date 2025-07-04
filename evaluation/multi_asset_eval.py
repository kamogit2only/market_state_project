import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from backtest.runner import backtest
from metrics import calc_metrics
from policy.selector_mix import select_mixed

SYMS = {"^N225": "N225", "^GSPC": "SPX", "AAPL": "AAPL", "BTC-USD": "BTC"}
pars = dict(trend_w=0.5, hurst_thr=0.55, vr_p_thr=0.01, mom_lb=20, mr_z=1.0)

rows, curves = {}, {}
for s, tag in SYMS.items():
    p = yf.download(s, start="2020-01-01")["Close"]
    sig = select_mixed(p, **pars).generate_signals()
    eq = backtest(p, sig)["equity"]
    curves[tag + "-Mix"] = eq
    bh = backtest(p, pd.Series(1, index=p.index))["equity"]
    rows[tag + "-BH"] = calc_metrics(bh)
    rows[tag + "-Mix"] = calc_metrics(eq)

pd.DataFrame(rows).T.to_csv("reports/multi_asset_report.csv")
pd.DataFrame(curves).plot(title="Mixed Strategy Equity Curves")
plt.savefig("reports/multi_asset_equity.png")
plt.close()
print("multi_asset_report.csv と equity.png を生成しました")
