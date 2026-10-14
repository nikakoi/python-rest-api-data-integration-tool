"""Fetch records from a JSON REST API and export selected fields to CSV."""

from __future__ import annotations

import argparse
import csv
import logging
from pathlib import Path
from typing import Any

import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"
FIELDS = ("id", "userId", "title", "body")
logger = logging.getLogger(__name__)


def fetch_records(url: str = API_URL, timeout: float = 10.0) -> list[dict[str, Any]]:
    """Fetch a JSON array of objects, raising useful errors on failed responses."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.Timeout as exc:
        raise RuntimeError(f"Request timed out after {timeout} seconds") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"API request failed: {exc}") from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("API returned invalid JSON") from exc
    if not isinstance(payload, list) or any(not isinstance(row, dict) for row in payload):
        raise RuntimeError("Expected the API to return a JSON array of objects")
    logger.info("Fetched %d records from %s", len(payload), url)
    return payload


def export_csv(records: list[dict[str, Any]], output_path: str | Path) -> int:
    """Write only the configured fields; absent values are written as empty cells."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    logger.info("Exported %d records to %s", len(records), path)
    return len(records)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=API_URL, help="JSON API endpoint")
    parser.add_argument("--output", default="data/posts.csv", help="Destination CSV path")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        count = export_csv(fetch_records(args.url, args.timeout), args.output)
    except RuntimeError as exc:
        logger.error("%s", exc)
        return 1
    print(f"Exported {count} records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
