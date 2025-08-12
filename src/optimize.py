import os
import itertools
import pandas as pd
from pathlib import Path

from .data import load_bars, add_features
from .strategy import SmaCross
from .backtest import backtest_long_only, Costs

def run_grid(ticker: str, start: str, fast_list, slow_list):
    bars = load_bars(ticker, start=start)
    rows = []
    for f, s in itertools.product(fast_list, slow_list):
        if f >= s:  # only sensible pairs
            continue
        feats = add_features(bars, fast=f, slow=s)
        sigs = SmaCross().generate(feats)
        res = backtest_long_only(feats, sigs, init_capital=10_000.0, costs=Costs(slippage_bps=2.0))
        m = res.metrics
        rows.append({
            "FAST": f, "SLOW": s,
            "CAGR": m["CAGR"],
            "Sharpe": m["Sharpe"],
            "MaxDrawdown": m["MaxDrawdown"],
            "FinalEquity": m["FinalEquity"],
            "Turnover_per_bar": m["Turnover_per_bar"],
            "NumTrades": m["NumTrades"],
        })
    return pd.DataFrame(rows).sort_values(["Sharpe","CAGR"], ascending=[False, False])

def main():
    ticker = os.environ.get("TICKER", "AAPL").upper()
    start = os.environ.get("START", "2018-01-01")

    # tweak these lists as you like
    fast_list = [5, 10, 20, 30, 50]
    slow_list = [50, 100, 150, 200, 250]

    print(f"Running grid for {ticker} from {start}...")
    df = run_grid(ticker, start, fast_list, slow_list)

    outdir = Path("output"); outdir.mkdir(exist_ok=True)
    path = outdir / "params_grid.csv"
    df.to_csv(path, index=False)
    print(f"Saved grid results to {path}")

    # show top 10 in console
    top = df.head(10)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 120):
        print("\nTop results by Sharpe:")
        print(top)

if __name__ == "__main__":
    main()
