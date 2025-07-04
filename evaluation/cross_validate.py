"""
学習: 2015-01-01〜2019-12-31 でグリッドサーチ
テスト: 2020-01-01〜2024-12-31 で最良パラメータを固定し評価
結果を ./reports/oos_report.csv へ保存
"""
import itertools, pandas as pd, yfinance as yf
from metrics import calc_metrics
from policy.selector import select_strategy
from backtest.runner import backtest

GRID = {
    "hurst_thr": [0.55, 0.60, 0.65],
    "vr_p":      [0.05, 0.01],
    "mom_lb":    [20, 40, 60],
    "mr_z":      [1.0, 1.5, 2.0],
}
SYMBOL = "^N225"
TRAIN_FROM, TRAIN_TO = "2015-01-01", "2019-12-31"
TEST_FROM,  TEST_TO  = "2020-01-01", "2024-12-31"

# ---------- データ取得 ----------
train_price = yf.download(SYMBOL, start=TRAIN_FROM, end=TRAIN_TO)["Close"]
test_price  = yf.download(SYMBOL, start=TEST_FROM,  end=TEST_TO)["Close"]

def run_policy(price, pars):
    equity, idx = [], []
    for i in range(200, len(price)):
        sub = price.iloc[: i + 1]
        strat = select_strategy(sub, *pars)
        sig   = strat.generate_signals()
        eq = backtest(sub, sig)["equity"].iloc[-1]
        equity.append(eq)
        idx.append(price.index[i])
    return pd.Series(equity, index=idx)

# ---------- グリッドサーチ（学習期間） ----------
best, best_pars = -1e9, None
for combo in itertools.product(*GRID.values()):
    eq = run_policy(train_price, combo)
    sharpe = calc_metrics(eq)["sharpe"]
    if sharpe > best:
        best, best_pars = sharpe, combo

print("Best params (train):", dict(zip(GRID.keys(), best_pars)), "Sharpe:", round(best, 3))

# ---------- テスト期間評価 ----------
policy_eq = run_policy(test_price, best_pars)
bh_sig    = pd.Series(1, index=test_price.index)  # Buy&Hold
bh_eq     = backtest(test_price, bh_sig)["equity"]

rows = {
    "Buy&Hold": calc_metrics(bh_eq),
    "Policy":   calc_metrics(policy_eq),
}
df = pd.DataFrame(rows).T
df.to_csv("reports/oos_report.csv")
print(df) 