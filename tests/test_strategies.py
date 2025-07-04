import pandas as pd, numpy as np
from strategies.hold import HoldStrategy
from strategies.momentum import MomentumStrategy

def test_hold_signal():
    price = pd.Series(np.arange(10.0))
    sig = HoldStrategy(price).generate_signals()
    assert sig.eq(1).all()

def test_momentum_runs():
    price = pd.Series(np.arange(30.0))
    sig = MomentumStrategy(price, lookback=5).generate_signals()
    assert set(sig.unique()) <= {0,1} 