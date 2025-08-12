import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
from .data import load_bars, add_features
from .strategy import SmaCross
from .backtest import backtest_long_only, Costs

def main():
    ticker = os.environ.get("TICKER", "AAPL")
    start = os.environ.get("START", "2018-01-01")
    fast = int(os.environ.get("FAST", "20"))
    slow = int(os.environ.get("SLOW", "50"))

    print(f"Downloading {ticker} from {start}...")
    bars = load_bars(ticker, start=start)
    feats = add_features(bars, fast=fast, slow=slow)

    sigs = SmaCross().generate(feats)
    res = backtest_long_only(
        feats, sigs, init_capital=10_000.0, costs=Costs(slippage_bps=2.0)
    )

        # --- Benchmark & drawdown ---
    bh_equity = (1 + feats["ret"].fillna(0.0)).cumprod() * 10_000
    dd = res.equity / res.equity.cummax() - 1.0

    # Ensure output folder exists
    outdir = Path("output"); outdir.mkdir(exist_ok=True)

    # --- Price with SMA lines + trade markers ---
    print("STEP: making trade chart...")
    price = feats["close"]
    sma_f = feats["sma_fast"]
    sma_s = feats["sma_slow"]

    w = sigs.weight.reindex(feats.index).fillna(0.0)
    trades = w.diff().fillna(w)
    buy_idx = trades > 0
    sell_idx = trades < 0

    plt.figure()
    price.plot(label="Close", alpha=0.7)
    sma_f.plot(label=f"SMA {fast}", linewidth=1.5)
    sma_s.plot(label=f"SMA {slow}", linewidth=1.5)
    plt.scatter(price.index[buy_idx], price[buy_idx], marker="^", s=60, label="Buy", zorder=3)
    plt.scatter(price.index[sell_idx], price[sell_idx], marker="v", s=60, label="Sell", zorder=3)
    plt.title(f"Price + SMAs + Trades — {ticker}")
    plt.xlabel("Date"); plt.ylabel("Price")
    plt.legend(); plt.tight_layout()
    trade_path = outdir / "price_sma_trades.png"
    plt.savefig(trade_path)
    print(f"Saved chart to {trade_path}")

    # --- Metrics ---
    print("=== Metrics ===")
    for k, v in res.metrics.items():
        try:
            print(f"{k:15s}: {v:.4f}")
        except Exception:
            print(f"{k:15s}: {v}")

    # --- Equity: Strategy vs Buy & Hold ---
    print("STEP: making equity chart...")
    plt.figure()
    res.equity.plot(label="Strategy")
    bh_equity.plot(label="Buy & Hold")
    plt.ylabel("Equity ($)")
    plt.xlabel("Date")
    plt.title(f"Equity — {ticker} (SMA {fast}/{slow})")
    plt.legend(); plt.tight_layout()
    eq_path = outdir / "equity_curve.png"
    plt.savefig(eq_path)
    print(f"Saved chart to {eq_path}")

    # --- Drawdown chart ---
    print("STEP: making drawdown chart...")
    plt.figure()
    dd.plot()
    plt.ylabel("Drawdown")
    plt.xlabel("Date")
    plt.title("Strategy Drawdown")
    plt.tight_layout()
    dd_path = outdir / "drawdown.png"
    plt.savefig(dd_path)
    print(f"Saved chart to {dd_path}")



if __name__ == "__main__":
    main()
