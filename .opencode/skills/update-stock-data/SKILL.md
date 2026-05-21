---
name: update-stock-data
description: Use when working in this repository to update US stock price CSVs from the configured watchlist, recalculate technical indicator data, validate outputs, or explain the data refresh workflow for local CLI agents such as OpenCode.
---

# Update Stock Data

Use this skill from the repository root of `stock_agent_works` when the user asks to update stock prices, refresh market data, calculate indicators, inspect the watchlist, or validate generated CSV output.

## Repository Contract

- Watchlist: `config/us_stock.csv`, one ticker per line.
- Raw data output: `data/<TICKER>.csv`.
- Processed data output: `data/processed/<TICKER>.csv`.
- Price collection script: `scripts/collect_daily_data.py`.
- Indicator calculation script: `scripts/calculate_indicators.py`.
- Output validation script: `scripts/validate_stock_outputs.py`.
- The scripts use relative paths, so run commands from the repository root.
- Market data comes from Yahoo Finance through `yfinance`; internet access is required for collection.

## Standard Workflow

1. Check the working tree before changing files:

   ```bash
   git status --short
   ```

2. Do not inspect `config/us_stock.csv` during a normal refresh. Only show or edit the ticker list when the user explicitly asks to inspect, list, add, remove, or change tickers.

   If the user explicitly asks to inspect the watchlist, run:

   ```bash
   sed -n '1,120p' config/us_stock.csv
   ```

3. Ensure dependencies are available:

   ```bash
   python -m pip install -r requirements.txt
   ```

   If a local virtual environment exists, prefer its Python:

   ```bash
   .venv/bin/python -m pip install -r requirements.txt
   ```

4. Collect the latest daily price data:

   ```bash
   python scripts/collect_daily_data.py
   ```

   Or with the local virtual environment:

   ```bash
   .venv/bin/python scripts/collect_daily_data.py
   ```

5. Recalculate indicators after collection:

   ```bash
   python scripts/calculate_indicators.py
   ```

   Or with the local virtual environment:

   ```bash
   .venv/bin/python scripts/calculate_indicators.py
   ```

## Validation

After running the scripts, verify that every configured ticker has raw CSV output, processed CSV output, and the expected indicator columns. Always use the validation script so the command prints a clear success or failure result:

```bash
python scripts/validate_stock_outputs.py
```

Or with the local virtual environment:

```bash
.venv/bin/python scripts/validate_stock_outputs.py
```

Expected indicator columns include:

- `MA10`
- `MA20`
- `MA55`
- `MACD`
- `MACD_Signal`
- `MACD_Hist`
- `ATR`
- `RSI`

## Important Behavior

- `collect_daily_data.py` overwrites each ticker's raw CSV with data from `2025-01-01` through the current date.
- `calculate_indicators.py` reads only CSV files directly under `data/`; it does not recursively process `data/processed/`.
- Moving averages, ATR, and RSI naturally contain blank values at the beginning of each file until the rolling windows have enough rows.
- If price collection fails, do not invent market data. Report the failed tickers and the command output.
- If only calculation is requested and current raw CSVs already exist, run only `scripts/calculate_indicators.py`.
- Do not loop on ticker inspection. A normal refresh should run collection, calculation, validation, then stop and report the result.
- Treat `validation ok: ...` from `scripts/validate_stock_outputs.py` as completion evidence.

## Response Pattern

When finished, report:

- commands run,
- tickers refreshed,
- output locations,
- any failed or missing tickers,
- validation performed.
