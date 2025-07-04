from indicators.randomness import detect_regime
from strategies.momentum import MomentumStrategy
from strategies.mean_revert import MeanRevertStrategy
from strategies.hold import HoldStrategy

def select_strategy(price_series):
    regime = detect_regime(price_series)
    if regime["trend"]:
        return MomentumStrategy(price_series)
    if regime["mean_revert"]:
        return MeanRevertStrategy(price_series)
    return HoldStrategy(price_series) 