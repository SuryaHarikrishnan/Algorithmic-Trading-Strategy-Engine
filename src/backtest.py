from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class Costs:
    commission_per_trade: float = 0.0
    slippage_bps: float = 2.0  # basis points per trade event

@dataclass
class Result:
    equity: pd.Series
    returns: pd.Series
    trades: pd.Series
    metrics: dict

def backtest_long_only(data: pd.DataFrame, signals, init_capital: float = 10_000.0, costs: Costs = Costs()) -> Result:
    # Inputs
    px = data["close"]
    ret = data["ret"].fillna(0.0)
    w = signals.weight.reindex(px.index).fillna(0.0)   # position 0..1

    # Trades are changes in position
    trades = w.diff().fillna(w)
    n_trades = trades.abs().sum()

    # Very simple slippage proxy (tiny per trade). You can improve later.
    slippage = (costs.slippage_bps / 1e4) * trades.abs() * 0
    gross = w * ret
    net_ret = gross - slippage.fillna(0.0)

    # Equity & drawdown
    equity = (1 + net_ret).cumprod() * init_capital
    dd = equity / equity.cummax() - 1.0

    # Metrics
    days = (px.index[-1] - px.index[0]).days
    years = max(days / 365.25, 1e-9)
    cagr = (equity.iloc[-1] / init_capital) ** (1 / years) - 1 if equity.iloc[0] > 0 else np.nan
    sharpe = np.sqrt(252) * net_ret.mean() / (net_ret.std() + 1e-12)
    calmar = - (cagr / dd.min()) if dd.min() < 0 else np.nan
    turnover = trades.abs().sum() / len(trades)

    metrics = {
        "CAGR": float(cagr),
        "Sharpe": float(sharpe),
        "MaxDrawdown": float(dd.min()),
        "Turnover_per_bar": float(turnover),
        "NumTrades": float(n_trades),
        "FinalEquity": float(equity.iloc[-1]),
    }

    return Result(equity=equity, returns=net_ret, trades=trades, metrics=metrics)
