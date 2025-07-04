import random
from policy.selector import select_strategy      # 既存裁定ロジック
from strategies.ema_cross import EMACrossStrategy
from strategies.donchian import DonchianStrategy
from strategies.bband_mr import BBandMRStrategy
from strategies.rsi_mr import RSIMRStrategy

def select_mixed(price, trend_w=0.7, hurst_thr=0.55, vr_p_thr=0.01,
                 mom_lb=20, mr_z=1.0):
    """
    1) 既存レジーム判定で Trend/MR を決定
    2) 決定グループ内で *trend_w* または (1−trend_w) で個別戦略を抽選
    """
    base = select_strategy(price, hurst_thr, vr_p_thr, mom_lb, mr_z)
    if isinstance(base, (EMACrossStrategy, DonchianStrategy)):
        # Trend 系 → EMA vs Donchian
        return EMACrossStrategy(price) if random.random() < 0.5 else DonchianStrategy(price)
    else:
        # MR 系 → BBand vs RSI
        return BBandMRStrategy(price) if random.random() < 0.5 else RSIMRStrategy(price) 