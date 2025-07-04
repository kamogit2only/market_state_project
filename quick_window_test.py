import yfinance as yf

from backtest.runner import backtest
from metrics import calc_metrics
from policy.selector_mix import select_mixed

# AAPLデータ取得（より長期間）
price = yf.download("AAPL", "2020-01-01", "2024-12-31")["Close"]
print(
    f"データ期間: {price.index[0].strftime('%Y-%m-%d')} 〜 {price.index[-1].strftime('%Y-%m-%d')}"
)
print(f"データ数: {len(price)}")

# 混合戦略でシグナル生成
pars = dict(trend_w=0.5, hurst_thr=0.55, vr_p_thr=0.01, mom_lb=20, mr_z=1.0)
sig = select_mixed(price, **pars).generate_signals()

# 信号頻度の分析
total_signals = int(sig.sum())
signal_freq = total_signals / len(sig) * 100
print("\n信号頻度分析:")
print(f"  総信号数: {total_signals}")
print(f"  信号頻度: {signal_freq:.2f}%")

# バックテスト実行
eq = backtest(price, sig)["equity"]
metrics = calc_metrics(eq)

print("\nパフォーマンス指標:")
print(f"  総リターン: {metrics['total_return']:.4f}")
print(f"  Sharpe比率: {metrics['sharpe']:.4f}")
print(f"  最大ドローダウン: {metrics['max_dd']:.4f}")

# 信号の時系列分布
print("\n信号分布:")
print(f"  0 (非保有): {len(sig[sig==0])} ({len(sig[sig==0])/len(sig)*100:.1f}%)")
print(f"  1 (保有): {len(sig[sig==1])} ({len(sig[sig==1])/len(sig)*100:.1f}%)")

# 最初と最後の10日間の信号を表示
print("\n最初の10日間の信号:")
print(sig.head(10).values)
print("\n最後の10日間の信号:")
print(sig.tail(10).values)
