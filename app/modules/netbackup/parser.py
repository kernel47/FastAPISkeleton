from typing import Any, Dict

from app.shared.case import keys_to_snake
from app.shared.parser import flatten_record


def with_raw(base: Dict[str, Any], raw: Dict[str, Any], include_raw: bool) -> Dict[str, Any]:
    if include_raw:
        base["raw"] = keys_to_snake(raw)
    return base


def parse_policy(record: Dict[str, Any], raw: bool = False) -> Dict[str, Any]:
    item = flatten_record(record)
    return with_raw(
        {
            "id": item.get("id") or item.get("policy_name") or item.get("policyname"),
            "policy_name": item.get("policy_name") or item.get("policyname") or item.get("name"),
            "policy_type": item.get("policy_type") or item.get("policytype") or item.get("type"),
            "active": item.get("active") if item.get("active") is not None else item.get("enabled"),
            "storage": item.get("storage") or item.get("storage_unit"),
            "clients": item.get("clients"),
            "schedules": item.get("schedules"),
        },
        item,
        raw,
    )


def parse_job(record: Dict[str, Any], raw: bool = False) -> Dict[str, Any]:
    item = flatten_record(record)
    return with_raw(
        {
            "id": item.get("id") or item.get("job_id") or item.get("jobid"),
            "job_id": item.get("job_id") or item.get("jobid") or item.get("id"),
            "state": item.get("state") or item.get("status"),
            "status_code": item.get("status_code") if item.get("status_code") is not None else item.get("status"),
            "policy_name": item.get("policy_name") or item.get("policyname"),
            "client_name": item.get("client_name") or item.get("clientname"),
            "start_time": item.get("start_time") or item.get("starttime"),
            "end_time": item.get("end_time") or item.get("endtime"),
        },
        item,
        raw,
    )


def parse_image(record: Dict[str, Any], raw: bool = False) -> Dict[str, Any]:
    item = flatten_record(record)
    return with_raw(
        {
            "id": item.get("id") or item.get("backup_id") or item.get("backupid"),
            "backup_id": item.get("backup_id") or item.get("backupid") or item.get("id"),
            "client_name": item.get("client_name") or item.get("clientname"),
            "policy_name": item.get("policy_name") or item.get("policyname"),
            "schedule_type": item.get("schedule_type") or item.get("scheduletype"),
            "backup_time": item.get("backup_time") or item.get("backuptime"),
            "expiration_time": item.get("expiration_time") or item.get("expirationtime"),
        },
        item,
        raw,
    )
