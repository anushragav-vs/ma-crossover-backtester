# Moving Average Crossover Strategy Backtester

A Python backtesting engine that tests a classic trend-following strategy (20-day/50-day moving average crossover) on Alphabet Inc. (GOOG) stock, comparing it against a simple buy-and-hold benchmark across 10 years of daily price data.

## Overview

This project answers a simple question: would systematically buying when a short-term moving average crosses above a long-term moving average — and selling when it crosses back below — have outperformed just buying and holding the stock?

The short answer: no, not on a total-return basis. But the strategy did meaningfully reduce risk (lower volatility, smaller max drawdown), which is a real and important trade-off in quantitative finance. This project documents that trade-off with actual numbers rather than assuming a backtest "winning" is the only measure of success.

## Motivation

I built this as my first hands-on quant finance project, applying Python and pandas to a strategy concept I was already familiar with from discretionary trading experience. The goal was to build a properly structured backtest — including handling look-ahead bias — rather than a naive signal-following script.

## Features

- Automated data collection via Yahoo Finance (`yfinance`)
- Data cleaning and validation pipeline
- Exploratory data analysis (price trends, return distribution)
- Moving average crossover signal generation (bias-free, using next-day execution)
- Full backtest simulation with equity curve tracking
- Performance metrics: CAGR, annualized volatility, Sharpe ratio, maximum drawdown
- Multi-panel visualization: price/signals, equity curves, drawdown comparison

## Methodology

- **Signal**: Long when 20-day SMA > 50-day SMA, flat otherwise
- **Execution timing**: Signals are shifted forward one day before being acted on, to avoid look-ahead bias (you can only trade on a crossover the day *after* it's confirmed)
- **Benchmark**: Buy-and-hold GOOG over the same period

## Dataset

- **Source**: Yahoo Finance, via the `yfinance` Python library
- **Instrument**: GOOG (Alphabet Inc.)
- **Period**: January 2015 – December 2024 (daily bars)
- **Fields used**: Close price
- **Limitations**: Free data can have minor adjustment discrepancies; not suitable for live/production trading

## Results

| Metric | Strategy | Buy & Hold |
|---|---|---|
| CAGR | 11.63% | 22.30% |
| Annualized Volatility | 21.12% | 28.50% |
| Sharpe Ratio | 0.63 | 0.84 |
| Max Drawdown | -34.12% | -44.60% |



![Full Strategy Report](images/full_strategy_report.png)



**Interpretation**: The crossover strategy underperformed buy-and-hold on total return and risk-adjusted return (Sharpe), but reduced both volatility and maximum drawdown by a meaningful margin. This is a well-documented characteristic of simple trend-following strategies on strongly trending assets: they reduce downside pain but also miss part of the recovery after a dip, which caps their upside relative to buy-and-hold.

## Limitations

- No transaction costs or slippage included — real-world results would be worse than shown here for the strategy (every crossover is a real trade with real costs, while buy-and-hold trades zero times)
- Single asset tested (GOOG only); results are not necessarily generalizable to other stocks or asset classes
- No out-of-sample or walk-forward testing performed — parameters (20/50-day windows) were chosen a priori, not optimized on this data, but were also not validated on unseen data
- Past backtested performance does not guarantee future results

## Future Improvements

- Add transaction costs and slippage modeling
- Test across multiple assets/sectors to check robustness
- Walk-forward / out-of-sample validation
- Parameter sensitivity analysis (test different MA window combinations)
- Add position sizing and stop-loss/take-profit rules

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/ma-crossover-backtester.git
cd ma-crossover-backtester
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

## Usage

Run scripts in order from the project root:
bash
python src/get_data.py
python src/clean_data.py
python src/eda.py
python src/strategy.py
python src/backtest.py
python src/metrics.py
python src/visualize.py


## Technologies Used

- Python 3.11
- pandas, NumPy — data manipulation
- matplotlib — visualization
- yfinance — market data

## Project Structure


ma-crossover-backtester/
├── data/           # Raw and processed price data
├── images/         # Report-quality charts for README
├── results/        # EDA charts and performance metrics
├── src/            # All source code
├── requirements.txt
├── LICENSE
└── README.md


## Disclaimer

This project is for educational purposes only. It does not constitute financial advice, and backtested performance is not indicative of future real-world trading results.

## Author

Anush Ragav V S — First-year AI/ML student, building a quantitative finance portfolio.
```
