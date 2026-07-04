import csv
import json
from typing import Any, Dict, List, Optional


TEXT_FIELDS = ("tweet", "text", "full_text", "content", "body")


def parse_xquik_export(raw_export: str, filename: str = "tweets.json") -> List[str]:
    """Extract tweet text from a Xquik JSON, JSONL, or CSV export."""
    if not raw_export.strip():
        return []

    lowered_name = filename.lower()
    if lowered_name.endswith(".csv"):
        return _parse_csv(raw_export)
    if lowered_name.endswith(".jsonl"):
        return _parse_jsonl(raw_export)

    try:
        parsed = json.loads(raw_export)
    except json.JSONDecodeError:
        return _parse_jsonl(raw_export)

    return _texts_from_records(_records_from_json(parsed))


def _parse_csv(raw_export: str) -> List[str]:
    reader = csv.DictReader(raw_export.splitlines())
    if reader.fieldnames is None:
        return []

    text_field = _find_text_field(reader.fieldnames)
    if text_field is None:
        raise ValueError("Xquik CSV export needs a tweet, text, full_text, content, or body column.")

    return [_clean_text(row.get(text_field)) for row in reader if _clean_text(row.get(text_field))]


def _parse_jsonl(raw_export: str) -> List[str]:
    records: List[Dict[str, Any]] = []
    for line in raw_export.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError("Xquik JSONL export contains an invalid JSON line.") from exc
        if isinstance(parsed, dict):
            records.append(parsed)

    return _texts_from_records(records)


def _records_from_json(parsed: Any) -> List[Dict[str, Any]]:
    if isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, dict)]
    if isinstance(parsed, dict):
        for key in ("tweets", "items", "data", "results"):
            value = parsed.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [parsed]
    return []


def _texts_from_records(records: List[Dict[str, Any]]) -> List[str]:
    tweets: List[str] = []
    for record in records:
        text_field = _find_text_field(record.keys())
        if text_field is None:
            continue
        cleaned = _clean_text(record.get(text_field))
        if cleaned:
            tweets.append(cleaned)
    return tweets


def _find_text_field(fields: Any) -> Optional[str]:
    normalized_fields = {str(field).lower(): str(field) for field in fields}
    for candidate in TEXT_FIELDS:
        if candidate in normalized_fields:
            return normalized_fields[candidate]
    return None


def _clean_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())
