import pandas as pd

from utils.common import to_series as _to_series


def backtest(price: pd.Series, signals: pd.Series, fee: float = 0.0) -> pd.DataFrame:
    """Vectorised long-only backtest (full allocation)."""
    price = _to_series(price, price.index)
    signals = _to_series(signals, signals.index).fillna(0)

    # 取引は翌日始値約定と仮定
    pos = signals.shift().fillna(0).clip(0, 1)  # 1 or 0
    ret = price.pct_change().fillna(0)
    strat_ret = pos * ret - fee * pos.diff().abs().fillna(0)
    equity = (1 + strat_ret).cumprod()

    return pd.DataFrame({"ret": strat_ret, "equity": equity})
