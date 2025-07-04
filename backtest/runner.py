import pandas as pd
def backtest(price: pd.Series, signals: pd.Series, fee: float = 0.0) -> pd.DataFrame:
    """Vectorised backtest (long-only, full allocation)."""
    pos = signals.shift().fillna(0)
    ret = price.pct_change().fillna(0)
    strat_ret = pos * ret - fee * pos.diff().abs().fillna(0)
    equity = (1 + strat_ret).cumprod()
    return pd.DataFrame({"ret": strat_ret, "equity": equity}) 