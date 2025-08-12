from pathlib import Path
import pandas as pd
import yfinance as yf

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def load_bars(ticker: str, start: str = "2018-01-01", end: str | None = None, interval: str = "1d") -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end, interval=interval, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for {ticker}.")
    df = df.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]].dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df["ret"] = df["close"].pct_change()
    return df

def add_features(df: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.DataFrame:
    out = df.copy()
    out["sma_fast"] = out["close"].rolling(fast).mean()
    out["sma_slow"] = out["close"].rolling(slow).mean()
    out["vol_20"] = out["ret"].rolling(20).std()
    return out.dropna()
