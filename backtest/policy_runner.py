import pandas as pd
from policy.selector import select_strategy
from backtest.runner import backtest

def run_policy(price: pd.Series, window: int = 100) -> pd.DataFrame:
    equity = []
    idx = price.index
    for i in range(window, len(price)):
        sub = price[:i]
        strat = select_strategy(sub)
        sig = strat.generate_signals()
        bt = backtest(sub, sig)
        equity.append(bt["equity"].iloc[-1])
    return pd.DataFrame({"equity": equity}, index=idx[window:]) 