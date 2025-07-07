import itertools, pandas as pd, yfinance as yf
from policy.selector_mix import select_mixed
from backtest.runner import backtest
from metrics import calc_metrics
p = yf.download("7011.T","2018-01-01")["Close"]   # 三菱重工

grid_h = [0.45,0.50,0.55,0.60,0.65]
grid_v = [0.10,0.05,0.01]
res=[]
for h,v in itertools.product(grid_h,grid_v):
    sig = select_mixed(p, trend_w=0.5,
                       hurst_thr=h, vr_p_thr=v,
                       vol_scale=True).generate_signals()
    m = calc_metrics(backtest(p,sig)["equity"])
    m.update(hurst=h, vr_p=v, signals=int(sig.sum()))
    res.append(m)
df = pd.DataFrame(res).sort_values("sharpe",ascending=False)
df.to_csv("reports/regime_sens_mhi.csv", index=False)
print(df.head()) 