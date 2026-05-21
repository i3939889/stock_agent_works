# Stock Agent Works

Python utilities for collecting daily US stock price data and calculating technical indicators for a configured watchlist.

## Overview

This project reads ticker symbols from `config/us_stock.csv`, downloads daily historical price data from Yahoo Finance using `yfinance`, and writes CSV files under `data/`. A second script calculates common technical indicators and writes enriched CSV files under `data/processed/`.

The default data collection window starts on `2025-01-01` and ends on the current date.

## Project Structure

```text
.
├── config/
│   └── us_stock.csv              # One ticker symbol per line
├── data/
│   ├── <TICKER>.csv              # Raw daily OHLCV data
│   └── processed/
│       └── <TICKER>.csv          # Raw data plus technical indicators
├── docs/
│   └── design.txt                # Original feature notes
├── scripts/
│   ├── collect_daily_data.py     # Downloads daily stock data
│   └── calculate_indicators.py   # Calculates technical indicators
└── requirements.txt
```

## Requirements

- Python 3.9 or newer
- Internet access for downloading market data

Python dependencies are listed in `requirements.txt`:

- `yfinance`
- `pandas`

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configure Tickers

Edit `config/us_stock.csv` and put one ticker symbol on each line:

```text
MU
TSM
GOOGL
NVDA
PLTR
```

## Usage

Run commands from the repository root.

### 1. Collect Daily Price Data

```bash
python scripts/collect_daily_data.py
```

This creates or updates raw CSV files in `data/`, for example:

```text
data/NVDA.csv
data/TSM.csv
```

Raw files include columns such as:

- `Date`
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`
- `Dividends`
- `Stock Splits`

### 2. Calculate Technical Indicators

```bash
python scripts/calculate_indicators.py
```

This reads raw CSV files from `data/` and writes processed files to `data/processed/`.

Processed files include the original market data plus:

- `MA10`
- `MA20`
- `MA55`
- `MACD`
- `MACD_Signal`
- `MACD_Hist`
- `ATR`

## Notes

- The scripts use relative paths, so run them from the project root.
- `collect_daily_data.py` overwrites each ticker's raw CSV output with the latest downloaded data.
- `calculate_indicators.py` only reads CSV files directly under `data/`; it does not recursively process files under `data/processed/`.
- Market data availability and accuracy depend on Yahoo Finance through the `yfinance` package.

