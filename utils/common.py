import numpy as np
import pandas as pd


def to_series(arr, index):
    """1D 変換 & Series ラップ（全バックテスター共通）"""
    flat = np.asarray(arr).flatten()
    return pd.Series(flat, index=index)
