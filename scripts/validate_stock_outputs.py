from pathlib import Path

import pandas as pd


WATCHLIST = Path("config/us_stock.csv")
RAW_DIR = Path("data")
PROCESSED_DIR = RAW_DIR / "processed"
EXPECTED_INDICATORS = {
    "MA10",
    "MA20",
    "MA55",
    "MACD",
    "MACD_Signal",
    "MACD_Hist",
    "ATR",
    "RSI",
}


def read_tickers() -> list[str]:
    if not WATCHLIST.exists():
        raise SystemExit(f"missing watchlist: {WATCHLIST}")

    return [line.strip() for line in WATCHLIST.read_text().splitlines() if line.strip()]


def main() -> None:
    tickers = read_tickers()
    if not tickers:
        raise SystemExit("no tickers configured")

    missing: list[str] = []
    column_errors: list[str] = []

    for ticker in tickers:
        raw_path = RAW_DIR / f"{ticker}.csv"
        processed_path = PROCESSED_DIR / f"{ticker}.csv"

        if not raw_path.is_file() or raw_path.stat().st_size == 0:
            missing.append(f"missing raw: {ticker}")

        if not processed_path.is_file() or processed_path.stat().st_size == 0:
            missing.append(f"missing processed: {ticker}")
            continue

        df = pd.read_csv(processed_path, nrows=1)
        absent_columns = sorted(EXPECTED_INDICATORS.difference(df.columns))
        if absent_columns:
            column_errors.append(
                f"missing processed columns for {ticker}: {', '.join(absent_columns)}"
            )

    for item in missing:
        print(item)
    for item in column_errors:
        print(item)

    if missing or column_errors:
        raise SystemExit("validation failed")

    print(
        "validation ok: "
        f"{len(tickers)} tickers have raw CSVs, processed CSVs, and indicator columns"
    )


if __name__ == "__main__":
    main()
