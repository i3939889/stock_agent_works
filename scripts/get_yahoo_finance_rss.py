import argparse
import json
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


DEFAULT_RSS_URL = "https://finance.yahoo.com/news/rssindex"
DEFAULT_OUTPUT_DIR = "data"


def get_text(element, tag_name):
    child = element.find(tag_name)
    if child is None or child.text is None:
        return None
    return child.text.strip()


def parse_rss_datetime(value):
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).isoformat()
    except (TypeError, ValueError, IndexError):
        return value


def parse_yahoo_finance_rss(xml_content):
    root = ET.fromstring(xml_content)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS response did not include a channel element.")

    feed = {
        "title": get_text(channel, "title"),
        "link": get_text(channel, "link"),
        "description": get_text(channel, "description"),
        "language": get_text(channel, "language"),
        "last_build_date": parse_rss_datetime(get_text(channel, "lastBuildDate")),
        "items": [],
    }

    for item in channel.findall("item"):
        feed["items"].append(
            {
                "title": get_text(item, "title"),
                "link": get_text(item, "link"),
                "guid": get_text(item, "guid"),
                "description": get_text(item, "description"),
                "pub_date": parse_rss_datetime(get_text(item, "pubDate")),
                "source": get_text(item, "source"),
            }
        )

    return feed


def fetch_rss(url):
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; stock-agent-works/1.0; "
                "+https://finance.yahoo.com/news/rssindex)"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read()


def save_feed(feed, output_dir, source_url):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = os.path.join(output_dir, f"yf-rss-{timestamp}.json")

    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source_url": source_url,
        "feed": feed,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Yahoo Finance RSS news and save it as timestamped JSON."
    )
    parser.add_argument("--url", default=DEFAULT_RSS_URL, help="RSS feed URL to fetch.")
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for yf-rss-{datetime}.json output files.",
    )
    args = parser.parse_args()

    try:
        xml_content = fetch_rss(args.url)
        feed = parse_yahoo_finance_rss(xml_content)
        output_path = save_feed(feed, args.output_dir, args.url)
    except HTTPError as e:
        raise SystemExit(f"Failed to fetch RSS feed: HTTP {e.code} {e.reason}") from e
    except URLError as e:
        raise SystemExit(f"Failed to fetch RSS feed: {e.reason}") from e
    except ET.ParseError as e:
        raise SystemExit(f"Failed to parse RSS XML: {e}") from e
    except OSError as e:
        raise SystemExit(f"Failed to write JSON output: {e}") from e

    print(f"Saved {len(feed['items'])} RSS items to {output_path}")


if __name__ == "__main__":
    main()
