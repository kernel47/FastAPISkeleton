from typing import Any, Dict, List

from pydantic import BaseModel


class Page(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    limit: int
    offset: int
