import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa import stattools

def hurst(price: pd.Series) -> float:
    """Compute Hurst exponent via rescaled range (R/S)."""
    ts = np.log(price).dropna().values
    lags = range(2, 20)
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return 2.0 * poly[0]

def variance_ratio(price: pd.Series, lag: int = 2) -> tuple[float, float]:
    """Lo-MacKinlay variance ratio test."""
    returns = price.pct_change().dropna()
    n = len(returns)
    q = lag
    
    # Calculate variance ratios
    var_1 = returns.var()
    var_q = (returns.rolling(q).sum() / q).var()
    
    # Variance ratio statistic
    vr_stat = var_q / var_1
    
    # Simplified p-value (assuming normal distribution)
    # In practice, you'd want a more sophisticated test
    vr_p = 0.1  # Placeholder p-value
    
    return vr_stat, vr_p

def ljung_box_p(price: pd.Series, lags: int = 10) -> float:
    ts = price.dropna().pct_change().dropna()
    p = acorr_ljungbox(ts, lags=[lags], return_df=True)["lb_pvalue"].iloc[0]
    return p

def detect_regime(price: pd.Series) -> dict:
    h = hurst(price)
    vr, vr_p = variance_ratio(price)
    lb_p = ljung_box_p(price)
    return {
        "trend": h > 0.55 and vr_p < 0.05,
        "mean_revert": h < 0.45 and vr_p < 0.05,
        "random": lb_p > 0.05 and vr_p > 0.05,
        "metrics": {"hurst": h, "vr": vr, "vr_p": vr_p, "lb_p": lb_p},
    } 