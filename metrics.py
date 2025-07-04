import numpy as np, pandas as pd
def calc_metrics(equity: pd.Series, rf: float = 0.0) -> dict:
    ret = equity.pct_change().dropna()
    total_ret = equity.iloc[-1] / equity.iloc[0] - 1
    sharpe = np.sqrt(252) * (ret.mean() - rf/252) / ret.std(ddof=0)
    dd = (equity / equity.cummax() - 1).min()
    return {"total_return": total_ret, "sharpe": sharpe, "max_dd": dd} 