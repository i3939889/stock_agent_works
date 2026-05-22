---
name: major-market-quotes
description: Use when working in this repository to fetch or summarize latest major market quotes for ^GSPC, ^IXIC, ^DJI, ^RUT, ^VIX, ^TNX, CL=F, and GC=F using scripts/get_major_market_quotes.py and yfinance.
---

# Major Market Quotes

Use this skill from the repository root of `stock_agent_works` when the user asks for latest major index quotes, market snapshot data, equity index levels, VIX, 10-year yield proxy, crude oil futures, gold futures, or a market quote summary based on local yfinance output.

## Repository Contract

- Quote script: `scripts/get_major_market_quotes.py`.
- Default symbols: `^GSPC`, `^IXIC`, `^DJI`, `^RUT`, `^VIX`, `^TNX`, `CL=F`, `GC=F`.
- Default JSON output: `data/major-market-quotes-YYYYmmdd-HHMMSS.json`.
- Market data comes from Yahoo Finance through `yfinance`; internet access is required.
- The script uses relative paths, so run commands from the repository root.

## Standard Workflow

1. Fetch and save the latest default quote set:

   ```bash
   python3 scripts/get_major_market_quotes.py
   ```

2. For a quick check without writing a JSON file:

   ```bash
   python3 scripts/get_major_market_quotes.py --no-save
   ```

3. Use the newest quotes JSON file unless the user names a specific file:

   ```bash
   ls -t data/major-market-quotes-*.json | head -1
   ```

4. Read the JSON and base any report on `quotes`. Treat `symbol`, `last_price`, `quote_time`, `quote_interval`, `previous_close`, `change`, `change_percent`, `currency`, and `fetched_at` as primary evidence.

## Custom Symbols

If the user asks for a different symbol set, pass a comma-separated list:

```bash
python3 scripts/get_major_market_quotes.py --symbols "^GSPC,^IXIC,CL=F"
```

## Response Guidance

- Report the fetch timestamp, symbols covered, and output file path.
- Include each quote's `quote_time` when the user asks for current/latest quote detail.
- Mention any quote entries with a non-empty `error` field.
- Do not present yfinance values as exchange-direct real-time data; describe them as Yahoo Finance/yfinance quotes that may be delayed.
- Do not give personalized investment advice.
- If writing a market snapshot, separate equity indices, volatility/rates, and commodities.
