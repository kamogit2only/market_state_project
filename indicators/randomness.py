import numpy as np
import pandas as pd
import scipy.stats as scs
from statsmodels.stats.diagnostic import acorr_ljungbox


def hurst(price: pd.Series) -> float:
    """Compute Hurst exponent via rescaled range (R/S)."""
    ts = np.log(price).dropna().values
    lags = range(2, 20)
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return 2.0 * poly[0]


# ──────────────────────────────────────────────────────────────
# Lo-MacKinlay Variance Ratio (asymptotic Z-test)
# Ref: Lo, A., & MacKinlay, C. (1988)  "Stock Prices Do Not Follow RWs"
# ──────────────────────────────────────────────────────────────
def variance_ratio(price: pd.Series, lag: int = 2):
    r = price.pct_change().dropna().values.astype(float)
    n = r.size
    mu = r.mean()
    m = (n - lag + 1) * (1 - lag / n)
    if m <= 0:
        return np.nan, 1.0
    # lag期間リターン
    r_lag = np.array([np.sum(r[i : i + lag]) for i in range(n - lag + 1)])
    var_lag = np.var(r_lag, ddof=1)
    var_1 = np.var(r, ddof=1)
    if var_1 == 0:
        return np.nan, 1.0
    vr = var_lag / (lag * var_1)
    var_vr = (2 * (2 * lag - 1) * (lag - 1)) / (3 * lag * n)
    z = (vr - 1) / np.sqrt(var_vr) if var_vr > 0 else 0.0
    p = 2 * (1 - scs.norm.cdf(abs(z)))
    return vr, p


def ljung_box_p(price: pd.Series, lags: int = 10) -> float:
    ts = price.pct_change().dropna()
    return acorr_ljungbox(ts, lags=[lags], return_df=True)["lb_pvalue"].iloc[0]


def detect_regime(price: pd.Series) -> dict:
    """Return only raw metrics; interpretation is deferred to selector."""
    h = hurst(price)
    vr, vr_p = variance_ratio(price)
    lb_p = ljung_box_p(price)
    return {"metrics": {"hurst": h, "vr": vr, "vr_p": vr_p, "lb_p": lb_p}}
