import yfinance as yf
from pathlib import Path

def fetch(symbol="^N225", period="5y", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval)
    Path("data").mkdir(exist_ok=True)
    out = f"data/{symbol.strip('^')}.csv"
    df.to_csv(out)
    return out

if __name__ == "__main__":
    print(fetch())
