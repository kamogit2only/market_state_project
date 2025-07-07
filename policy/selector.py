from indicators.randomness import detect_regime
from strategies.hold import HoldStrategy
from strategies.mean_revert import MeanRevertStrategy
from strategies.momentum import MomentumStrategy


def select_strategy(price,
                    hurst_thr: float = 0.45,   # relaxed
                    vr_p_thr: float = 0.10,
                    mom_lb: int = 20,
                    mr_z: float = 1.0):
    m = detect_regime(price)["metrics"]
    # トレンド判定 → Momentum
    if m["hurst"] > hurst_thr and m["vr_p"] < vr_p_thr:
        return MomentumStrategy(price, lookback=mom_lb)
    # 逆張り判定 → Mean-revert
    if m["hurst"] < (1 - hurst_thr) and m["vr_p"] < vr_p_thr:
        return MeanRevertStrategy(price, z=mr_z)
    # それ以外 → Hold
    return HoldStrategy(price)
