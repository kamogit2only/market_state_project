from pathlib import Path

import yfinance as yf


def fetch(symbol="7011.T", period="5y", interval="1d"):  # 三菱重工
    df = yf.download(symbol, period=period, interval=interval)
    Path("data").mkdir(exist_ok=True)
    out = f"data/{symbol.strip('^')}.csv"
    df.to_csv(out)
    return out


if __name__ == "__main__":
    print(fetch())
