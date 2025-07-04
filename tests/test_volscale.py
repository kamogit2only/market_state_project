import numpy as np
import pandas as pd

from strategies.bband_mr import BBandMRStrategy
from strategies.donchian import DonchianStrategy
from strategies.rsi_mr import RSIMRStrategy

price = pd.Series(np.random.rand(300) + 100)
assert DonchianStrategy(price, vol_scale=True).generate_signals().isin([0, 1]).all()
assert BBandMRStrategy(price, vol_scale=True).generate_signals().isin([0, 1]).all()
assert RSIMRStrategy(price, vol_scale=True).generate_signals().isin([0, 1]).all()
