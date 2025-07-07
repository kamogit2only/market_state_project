import itertools, pandas as pd, yfinance as yf
from policy.selector_mix import select_mixed
from backtest.runner import backtest
from metrics import calc_metrics
SYMS = {
    "8035.T":"TEL","6861.T":"KEY","6758.T":"SONY",
    "7203.T":"TOY","9983.T":"FRT","2802.T":"AJI",
    "7011.T":"MHI","6501.T":"HIT","7012.T":"KHI",
    "9501.T":"TEP","9532.T":"OSG","5020.T":"ENE",
    "4502.T":"TAK","4523.T":"EIS","7733.T":"OLY"
}
grid_h = [0.35,0.40,0.45]
grid_v = [0.20,0.15,0.10]
rows=[]
for code, tag in SYMS.items():
    price = yf.download(code,"2020-01-01")["Close"]
    for h,v in itertools.product(grid_h,grid_v):
        sig = select_mixed(price, trend_w=0.5,
                           hurst_thr=h, vr_p_thr=v,
                           vol_scale=True).generate_signals()
        m = calc_metrics(backtest(price,sig)["equity"])
        m.update(ticker=tag, hurst=h, vr_p=v, signals=int(sig.sum()))
        rows.append(m)
pd.DataFrame(rows).to_csv("reports/regime_grid_step2.csv", index=False)
print("saved reports/regime_grid_step2.csv") 