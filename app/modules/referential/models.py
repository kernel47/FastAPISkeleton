from typing import Any, Dict

from pydantic import BaseModel


class MasterServer(BaseModel):
    hostname: str
    base_url: str
    username: str
    password: str
    region: str = ""
    locality: str = ""
    datacentre: str = ""
    is_baas: bool = False
    is_raas: bool = False
    domain_name: str = ""
    domain_type: str = ""
    raw: Dict[str, Any] = {}
