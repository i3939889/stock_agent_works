import argparse
import json
import os
from datetime import datetime, timezone

import yfinance as yf


DEFAULT_SYMBOLS = ["^GSPC", "^IXIC", "^DJI", "^RUT", "^VIX", "^TNX", "CL=F", "GC=F"]
DEFAULT_OUTPUT_DIR = "data"


def as_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def safe_fast_info(ticker):
    try:
        return dict(ticker.fast_info)
    except Exception:
        return {}


def timestamp_to_iso(value):
    if value is None:
        return None
    try:
        return value.to_pydatetime().isoformat()
    except AttributeError:
        return str(value)


def latest_history_snapshot(ticker, period, interval, include_previous_close):
    try:
        history = ticker.history(period=period, interval=interval)
    except Exception:
        return {}

    if history.empty:
        return {}

    last_row = history.iloc[-1]
    previous_close = None
    if include_previous_close and len(history) >= 2:
        previous_close = as_float(history.iloc[-2].get("Close"))

    return {
        "last_price": as_float(last_row.get("Close")),
        "previous_close": previous_close,
        "open": as_float(last_row.get("Open")),
        "day_high": as_float(last_row.get("High")),
        "day_low": as_float(last_row.get("Low")),
        "volume": as_int(last_row.get("Volume")),
        "quote_time": timestamp_to_iso(history.index[-1]),
        "quote_interval": interval,
    }


def history_fallback(ticker):
    snapshot = latest_history_snapshot(
        ticker, period="5d", interval="1m", include_previous_close=False
    )
    if snapshot:
        return snapshot
    return latest_history_snapshot(
        ticker, period="5d", interval="1d", include_previous_close=True
    )


def calculate_change(last_price, previous_close):
    if last_price is None or previous_close in (None, 0):
        return None, None

    change = last_price - previous_close
    change_percent = (change / previous_close) * 100
    return change, change_percent


def fetch_quote(symbol):
    ticker = yf.Ticker(symbol)
    fast_info = safe_fast_info(ticker)

    quote = {
        "symbol": symbol,
        "name": fast_info.get("shortName") or fast_info.get("longName"),
        "currency": fast_info.get("currency"),
        "exchange": fast_info.get("exchange"),
        "timezone": fast_info.get("timezone"),
        "last_price": as_float(fast_info.get("lastPrice")),
        "previous_close": as_float(fast_info.get("previousClose")),
        "open": as_float(fast_info.get("open")),
        "day_high": as_float(fast_info.get("dayHigh")),
        "day_low": as_float(fast_info.get("dayLow")),
        "year_high": as_float(fast_info.get("yearHigh")),
        "year_low": as_float(fast_info.get("yearLow")),
        "volume": as_int(fast_info.get("lastVolume")),
        "quote_time": None,
        "quote_interval": None,
        "source": "yfinance",
        "error": None,
    }

    fallback = history_fallback(ticker)
    for key, value in fallback.items():
        if quote.get(key) is None:
            quote[key] = value

    quote["change"], quote["change_percent"] = calculate_change(
        quote["last_price"], quote["previous_close"]
    )

    if quote["last_price"] is None:
        quote["error"] = "No quote data returned by yfinance."

    return quote


def fetch_quotes(symbols):
    quotes = []
    for symbol in symbols:
        try:
            quotes.append(fetch_quote(symbol))
        except Exception as e:
            quotes.append(
                {
                    "symbol": symbol,
                    "source": "yfinance",
                    "error": str(e),
                }
            )
    return quotes


def save_quotes(quotes, output_dir, symbols):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = os.path.join(output_dir, f"major-market-quotes-{timestamp}.json")

    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "symbols": symbols,
        "quotes": quotes,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return output_path, payload


def print_summary(quotes):
    for quote in quotes:
        symbol = quote.get("symbol")
        if quote.get("error"):
            print(f"{symbol}: error: {quote['error']}")
            continue

        last_price = quote.get("last_price")
        change = quote.get("change")
        change_percent = quote.get("change_percent")
        quote_time = quote.get("quote_time") or "time unavailable"

        if change is None or change_percent is None:
            print(f"{symbol}: {last_price} at {quote_time}")
        else:
            print(
                f"{symbol}: {last_price:.4f} "
                f"({change:+.4f}, {change_percent:+.2f}%) at {quote_time}"
            )


def parse_symbols(value):
    return [symbol.strip() for symbol in value.split(",") if symbol.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="Fetch latest major market index, rate, and commodity quotes with yfinance."
    )
    parser.add_argument(
        "--symbols",
        default=",".join(DEFAULT_SYMBOLS),
        help="Comma-separated symbols to fetch. Defaults to major market symbols.",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for major-market-quotes-{datetime}.json output files.",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Print a summary without writing a JSON output file.",
    )
    args = parser.parse_args()

    symbols = parse_symbols(args.symbols)
    if not symbols:
        raise SystemExit("No symbols provided.")

    quotes = fetch_quotes(symbols)
    print_summary(quotes)

    if not args.no_save:
        output_path, _ = save_quotes(quotes, args.output_dir, symbols)
        print(f"Saved {len(quotes)} quotes to {output_path}")


if __name__ == "__main__":
    main()
