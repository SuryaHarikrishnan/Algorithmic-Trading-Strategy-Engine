Alright — here’s the same README in plain text without any markdown `##` headers so you can copy it directly into GitHub without worrying about formatting symbols.

---

# Algo Engine — SMA Backtesting Tool

Overview
Algo Engine is a Python-based backtesting framework for simple moving average (SMA) crossover trading strategies.
It downloads historical price data, generates trade signals, and evaluates performance metrics such as CAGR, Sharpe ratio, drawdowns, and trade count.
The system also produces charts for equity growth, drawdowns, and trade entry/exit points.

Features

* Historical Data Download: Automatically fetches price data from Yahoo Finance.
* SMA Crossover Strategy: Configurable short-term (fast) and long-term (slow) moving averages.
* Backtesting Engine: Simulates trades, calculates metrics, and tracks portfolio equity.
* Performance Metrics:

  * Compound Annual Growth Rate (CAGR)
  * Sharpe Ratio
  * Maximum Drawdown
  * Turnover per Bar
  * Number of Trades
  * Final Equity Value
* Visualizations:

  * Equity curve vs. Buy & Hold benchmark
  * Drawdown chart
  * Price chart with SMA lines and trade markers

Project Structure
algo\_engine/
│
├── data/                  # Stored historical data
├── output/                # Generated charts and backtest results
├── src/
│   ├── data.py             # Data loading and feature generation
│   ├── strategy.py         # SMA crossover strategy
│   ├── backtest.py         # Backtesting logic
│   └── run\_backtest.py     # Main execution script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

Installation

1. Clone the repository
   git clone [https://github.com/SuryaHarikrishnan/algo\_engine.git](https://github.com/SuryaHarikrishnan/algo_engine.git)
   cd algo\_engine

2. Create a virtual environment
   python -m venv .venv

3. Activate the virtual environment
   Windows (PowerShell):
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ..venv\Scripts\Activate.ps1

Mac/Linux:
source .venv/bin/activate

4. Install dependencies
   pip install -r requirements.txt

Usage
Run the backtest with default parameters:
python -m src.run\_backtest

Customize parameters via environment variables:
TICKER=MSFT START=2020-01-01 FAST=10 SLOW=40 python -m src.run\_backtest

Output
The results will be saved in the output/ folder:

* equity\_curve.png — Strategy vs. Buy & Hold equity over time
* drawdown.png — Strategy drawdowns
* price\_sma\_trades.png — Price chart with SMA lines and trade entry/exit markers

Future Improvements

* Web-based dashboard for interactive analysis
* Multi-strategy backtesting
* Portfolio-level simulations
* Parameter optimization
