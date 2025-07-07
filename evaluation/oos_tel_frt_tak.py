import yfinance as yf, pandas as pd
from policy.selector_mix import select_mixed
from backtest.runner import backtest
from metrics import calc_metrics

SYMS = {"8035.T":"TEL","9983.T":"FRT","4502.T":"TAK"}
pars=dict(trend_w=0.5, vol_scale=True)

rows=[]
for code, tag in SYMS.items():
    p=yf.download(code,"2020-01-01", "2024-12-31", progress=False)["Close"]  # 2020-2024
    print(f"{tag} {code}: {p.index[0] if not p.empty else 'EMPTY'} ~ {p.index[-1] if not p.empty else 'EMPTY'} (len={len(p)})")
    if len(p) > 500:  # 十分なデータがある場合のみ分割
        train=p["2020":"2022"]; test=p["2023":"2024"]
    else:
        train=p; test=p  # データが少ない場合は全体を使用
    print(f"  train: {len(train)}, test: {len(test)}")
    # train 期間でパラ最適化は今回は省略、直に評価
    if len(test) > 100:  # 十分なデータがある場合のみ実行
        sig=select_mixed(test, **pars).generate_signals()
        m=calc_metrics(backtest(test,sig)["equity"])
        m["ticker"]=tag; rows.append(m)
    else:
        print(f"Warning: {tag} has insufficient data ({len(test)} points)")
pd.DataFrame(rows).to_csv("reports/oos_tel_frt_tak.csv", index=False)
print(pd.read_csv("reports/oos_tel_frt_tak.csv")) 