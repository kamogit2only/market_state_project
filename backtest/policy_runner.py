import pandas as pd
from policy.selector import select_strategy
from backtest.runner import backtest

def run_policy(price: pd.Series, window: int = 100) -> pd.DataFrame:
    """Rolling regime-switch backtest."""
    equities, dates = [], []
    for i in range(window, len(price)):
        sub = price.iloc[: i + 1]          # ← i まで含める
        strat = select_strategy(sub)
        sig = strat.generate_signals()

        # すべて NaN / 空 の場合はキャッシュ状態で代替
        if sig.isna().all():
            sig = pd.Series(0, index=sub.index)

        bt = backtest(sub, sig)
        equities.append(bt["equity"].iloc[-1])
        dates.append(price.index[i])

    return pd.DataFrame({"equity": equities}, index=dates) 