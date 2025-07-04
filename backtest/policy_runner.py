import pandas as pd
from policy.selector import select_strategy
from backtest.runner import backtest

def run_policy(price: pd.Series, window: int = 200,
               hurst_thr=0.55, vr_p_thr=0.05, mom_lb=20, mr_z=1.0):
    """Rolling regime-switch backtest."""
    equities, dates = [], []
    for i in range(window, len(price)):
        sub = price.iloc[: i + 1]          # ← i まで含める
        strat = select_strategy(sub, hurst_thr, vr_p_thr, mom_lb, mr_z)
        sig = strat.generate_signals()

        # すべて NaN / 空 の場合はキャッシュ状態で代替
        if sig.isna().all():
            sig = pd.Series(0, index=sub.index)
        
        # sigの長さがsubと一致しない場合は調整
        if len(sig) != len(sub):
            sig = sig.reindex(sub.index, fill_value=0)

        bt = backtest(sub, sig)
        equities.append(bt["equity"].iloc[-1])
        dates.append(price.index[i])

    return pd.DataFrame({"equity": equities}, index=dates) 