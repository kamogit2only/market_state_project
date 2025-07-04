import numpy as np
import pandas as pd
import yfinance as yf

from backtest.runner import backtest
from metrics import calc_metrics
from policy.selector_mix import select_mixed

price = yf.download("^N225", start="2020-01-01", end="2024-12-31")["Close"]
print(f"Price data length: {len(price)}")
pars = dict(hurst_thr=0.55, vr_p_thr=0.01, mom_lb=20, mr_z=1.0)

rows = []
for w in np.round(np.linspace(0, 1, 11), 2):
    print(f"Processing trend_weight: {w}")
    eq, idx = [], []
    for i in range(200, len(price)):
        sub = price.iloc[: i + 1]
        try:
            sig = select_mixed(sub, trend_w=w, **pars).generate_signals()
            bt_result = backtest(sub, sig)
            eq.append(bt_result["equity"].iloc[-1])
            idx.append(price.index[i])
        except Exception as e:
            print(f"  Error at i={i}: {e}")
            continue

    print(f"  Generated {len(eq)} equity points")
    if len(eq) > 0:
        equity_series = pd.Series(eq, index=idx)
        try:
            m = calc_metrics(equity_series)
            m["trend_weight"] = w
            rows.append(m)
            print(f"  Sharpe: {m['sharpe']:.3f}, Return: {m['total_return']:.3f}")
        except Exception as e:
            print(f"  Error in calc_metrics: {e}")
    else:
        print(f"  No data for trend_weight: {w}")

if len(rows) > 0:
    df = pd.DataFrame(rows).sort_values("sharpe", ascending=False)
    df.to_csv("reports/mix_grid_results.csv", index=False)
    print("\nTop 5 results:")
    print(df.head())
else:
    print("No results generated")
