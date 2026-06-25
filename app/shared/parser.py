from typing import Any, Dict, List

from app.shared.case import keys_to_snake


def extract_items(payload: Any) -> List[Dict[str, Any]]:
    payload = keys_to_snake(payload)
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in ("data", "items", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return [value]
    return [payload]


def extract_total(payload: Any, fallback: int = 0) -> int:
    payload = keys_to_snake(payload)
    if not isinstance(payload, dict):
        return fallback
    meta = payload.get("meta") or {}
    pagination = meta.get("pagination") or {}
    for container in (pagination, meta, payload):
        for key in ("total", "total_count", "count"):
            value = container.get(key)
            if isinstance(value, int):
                return value
    return fallback


def extract_next_after(payload: Any):
    payload = keys_to_snake(payload)
    if not isinstance(payload, dict):
        return None
    meta = payload.get("meta") or {}
    pagination = meta.get("pagination") or {}
    return pagination.get("after") or meta.get("after") or payload.get("after")


def flatten_record(record: Dict[str, Any]) -> Dict[str, Any]:
    record = keys_to_snake(record)
    attributes = record.get("attributes")
    result = {}
    if isinstance(attributes, dict):
        result.update(attributes)
    for key, value in record.items():
        if key not in ("attributes", "relationships", "links"):
            result.setdefault(key, value)
    return result
