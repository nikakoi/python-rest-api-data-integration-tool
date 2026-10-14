import csv
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

from api_to_csv import FIELDS, export_csv, fetch_records


def test_fetch_records_uses_timeout_and_returns_json(monkeypatch):
    response = Mock()
    response.json.return_value = [{"id": 1, "title": "Hello"}]
    monkeypatch.setattr("api_to_csv.requests.get", Mock(return_value=response))

    result = fetch_records("https://example.test/items", timeout=3)

    assert result == [{"id": 1, "title": "Hello"}]
    requests.get.assert_called_once_with("https://example.test/items", timeout=3)
    response.raise_for_status.assert_called_once()


def test_fetch_records_wraps_timeout(monkeypatch):
    monkeypatch.setattr("api_to_csv.requests.get", Mock(side_effect=requests.Timeout("slow")))
    with pytest.raises(RuntimeError, match="timed out"):
        fetch_records(timeout=0.1)


def test_fetch_records_wraps_http_error(monkeypatch):
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("404")
    monkeypatch.setattr("api_to_csv.requests.get", Mock(return_value=response))
    with pytest.raises(RuntimeError, match="API request failed"):
        fetch_records()


def test_fetch_records_rejects_non_array(monkeypatch):
    response = Mock()
    response.json.return_value = {"items": []}
    monkeypatch.setattr("api_to_csv.requests.get", Mock(return_value=response))
    with pytest.raises(RuntimeError, match="array of objects"):
        fetch_records()


def test_export_csv_writes_selected_fields_and_header(tmp_path: Path):
    destination = tmp_path / "nested" / "items.csv"
    records = [{"id": 7, "userId": 2, "title": "A", "body": "Text", "extra": "ignored"}]

    assert export_csv(records, destination) == 1
    with destination.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == list(FIELDS)
        assert next(reader) == {"id": "7", "userId": "2", "title": "A", "body": "Text"}


def test_export_csv_empty_records_still_writes_header(tmp_path: Path):
    destination = tmp_path / "empty.csv"
    assert export_csv([], destination) == 0
    assert destination.read_text(encoding="utf-8").strip() == ",".join(FIELDS)
