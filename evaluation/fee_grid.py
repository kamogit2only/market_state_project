import pandas as pd
import yfinance as yf

from backtest.runner import backtest
from metrics import calc_metrics
from policy.selector_mix import select_mixed

price = yf.download("^N225", "2020-01-01")["Close"]
pars = dict(trend_w=0.5, hurst_thr=0.55, vr_p_thr=0.01, mom_lb=20, mr_z=1.0)

rows = []
for fee in [0, 0.0005, 0.001]:
    sig = select_mixed(price, **pars).generate_signals()
    eq = backtest(price, sig, fee=fee)["equity"]
    m = calc_metrics(eq)
    m["fee"] = fee
    rows.append(m)

pd.DataFrame(rows).to_csv("reports/fee_grid.csv", index=False)
print(pd.read_csv("reports/fee_grid.csv"))
