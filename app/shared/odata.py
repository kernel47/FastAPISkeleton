from typing import Any, Dict, List, Optional

from app.shared.case import snake_to_camel


class QueryOptions:
    def __init__(
        self,
        limit: int = 100,
        offset: int = 0,
        filter: Optional[str] = None,
        raw: bool = False,
    ):
        self.limit = limit
        self.offset = offset
        self.filter = filter
        self.raw = raw


def simple_filters_to_odata(filters: Dict[str, Any]) -> Optional[str]:
    parts = []
    for key, value in filters.items():
        if value is None:
            continue
        parts.append("%s eq %s" % (snake_to_camel(key), odata_literal(value)))
    if not parts:
        return None
    return " and ".join(parts)


def combine_odata(base_filter: Optional[str], simple_filter: Optional[str]) -> Optional[str]:
    if base_filter and simple_filter:
        return "%s and %s" % (simple_filter, base_filter)
    return base_filter or simple_filter


def odata_literal(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return "'%s'" % str(value).replace("'", "''")


def netbackup_page_params(limit: int, offset: int, odata_filter: Optional[str] = None) -> Dict[str, Any]:
    params = {"page[limit]": limit, "page[offset]": offset}
    if odata_filter:
        params["filter"] = odata_filter
    return params


def netbackup_cursor_params(limit: int, after: Optional[str], odata_filter: Optional[str] = None) -> Dict[str, Any]:
    params = {"page[limit]": limit}
    if after:
        params["page[after]"] = after
    if odata_filter:
        params["filter"] = odata_filter
    return params
