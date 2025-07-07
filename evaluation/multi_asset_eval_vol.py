import yfinance as yf, pandas as pd
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
pars = dict(trend_w=0.5, hurst_thr=0.55, vr_p_thr=0.01,
            mom_lb=20, mr_z=1.0, vol_scale=True)

rows={}
for code, tag in SYMS.items():
    p = yf.download(code, start="2020-01-01")["Close"]
    sig = select_mixed(p, **pars).generate_signals()
    eq  = backtest(p, sig)["equity"]
    rows[tag] = calc_metrics(eq)

pd.DataFrame(rows).T.to_csv("reports/sector_vol_eval.csv")
print(pd.read_csv("reports/sector_vol_eval.csv")) 