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
pars=dict(trend_w=0.5, vol_scale=True)   # relaxed thr=0.45/0.10 via selector default
rows=[]
for code, tag in SYMS.items():
    p=yf.download(code,"2020-01-01")["Close"]
    strat=select_mixed(p, **pars)
    sig=strat.generate_signals()
    m=calc_metrics(backtest(p,sig)["equity"])
    m.update(ticker=tag, signals=int(sig.sum()))
    rows.append(m)
pd.DataFrame(rows).to_csv("reports/signal_stats_win15.csv",index=False)
print(pd.read_csv("reports/signal_stats_win15.csv")) 