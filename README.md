# Trading Examples

This repository includes a Python script demonstrating a simple Moving Average Crossover strategy for ETFs using data from Yahoo Finance.

## Requirements

- Python 3.8+
- [yfinance](https://pypi.org/project/yfinance/)
- pandas
- matplotlib

Install dependencies via pip:

```bash
pip install yfinance pandas matplotlib
```

## Usage

Run the script to download data for the iShares Core MSCI World ETF (`IWDA.DE`), calculate 50-day and 200-day moving averages, simulate the strategy, and plot the performance compared with a buy & hold approach:

```bash
python ma_crossover.py
```

The plot displays the cumulative returns of the strategy versus simply holding the ETF.
