---
name: yahoo-finance-market-brief
description: Use when working in this repository to fetch Yahoo Finance RSS with scripts/get_yahoo_finance_rss.py and write a concise market brief from the generated yf-rss JSON file.
---

# Yahoo Finance Market Brief

Use this skill from the repository root of `stock_agent_works` when the user asks for a Yahoo Finance RSS summary, daily market brief, market news brief, trading-day overview, or report based on Yahoo Finance RSS.

## Repository Contract

- RSS fetch script: `scripts/get_yahoo_finance_rss.py`.
- RSS source: `https://finance.yahoo.com/news/rssindex`.
- Default JSON output: `data/yf-rss-YYYYmmdd-HHMMSS.json`.
- The script uses relative paths, so run commands from the repository root.
- Internet access is required to fetch a new feed.

## Standard Workflow

1. Fetch a fresh Yahoo Finance RSS JSON file:

   ```bash
   python3 scripts/get_yahoo_finance_rss.py
   ```

2. Use the newest RSS JSON file unless the user names a specific file:

   ```bash
   ls -t data/yf-rss-*.json | head -1
   ```

3. Read the JSON and base the report on `feed.items`. Treat `title`, `source`, `pub_date`, and `link` as primary evidence. Use `description` only when present.

4. If the fetch fails, report the failure. Use an existing local `data/yf-rss-*.json` only when the user accepts a stale report or explicitly asks to use local data.

## Report Shape

Write a short, scan-friendly report with:

- **Market Brief**: 2-4 sentences on the dominant themes.
- **Top Themes**: 3-6 bullets grouping related stories, citing titles and sources.
- **Watch Points**: 3-5 bullets for macro, sector, company, rate, commodity, or geopolitical risks visible in the feed.
- **Notable Links**: 5-10 article links with title, source, and publication time.
- **Coverage Note**: feed timestamp, item count, and a note that the brief is derived from Yahoo Finance RSS rather than full-market price data.

## Guardrails

- Keep the tone neutral and analytical.
- Do not give personalized investment advice.
- Do not imply that RSS headlines alone prove market direction.
- Label inferences with wording such as "suggests", "points to", or "may indicate".
- Do not claim live prices, index moves, or earnings results unless those facts appear in the RSS item text.
- Do not add unsourced facts from memory unless the user asks for broader context; verify current facts when accuracy matters.

## Suggested Improvements

If the user asks to improve this workflow, suggest:

- Add a `--latest` or stable output filename option.
- Add a markdown report script that reads the newest JSON and writes `reports/market-brief-YYYYmmdd-HHMMSS.md`.
- Add tickers, sectors, and topic tags during RSS parsing.
- Store feeds under `data/news/` if the project accumulates more non-price data.
