from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.modules.referential.models import MasterServer
from app.shared.http import HttpClient
from app.shared.parser import extract_items, flatten_record


class ReferentialService:
    def __init__(self):
        self.http = HttpClient(settings.referential_base_url)

    async def list_master_servers(
        self,
        region: Optional[str] = None,
        locality: Optional[str] = None,
        datacentre: Optional[str] = None,
        is_baas: Optional[bool] = None,
        is_raas: Optional[bool] = None,
    ) -> List[MasterServer]:
        params = {
            "region": region,
            "locality": locality,
            "datacentre": datacentre,
            "is_baas": is_baas,
            "is_raas": is_raas,
        }
        payload = await self.http.get(settings.referential_master_servers_path, headers=self._headers(), params=params)
        return [self._master(item) for item in extract_items(payload)]

    async def get_master_server(self, hostname: str) -> MasterServer:
        path = settings.referential_master_server_path.format(hostname=hostname)
        payload = await self.http.get(path, headers=self._headers(), params={"hostname": hostname})
        items = extract_items(payload)
        if not items:
            raise ValueError("Master server not found: %s" % hostname)
        return self._master(items[0])

    async def resolve_many(self, hostnames: Optional[str]) -> List[MasterServer]:
        if not hostnames:
            return await self.list_master_servers()
        result = []
        for hostname in split_hostnames(hostnames):
            result.append(await self.get_master_server(hostname))
        return result

    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if settings.referential_token:
            token = settings.referential_token
            if settings.referential_token_prefix:
                token = "%s %s" % (settings.referential_token_prefix, token)
            headers[settings.referential_token_header] = token
        return headers

    def _master(self, payload: Dict[str, Any]) -> MasterServer:
        item = flatten_record(payload)
        hostname = first(item, "hostname", "host", "name")
        base_url = first(item, "base_url", "api_url", "url", "endpoint")
        username = first(item, "username", "login", "user", "user_name")
        password = first(item, "password", "passwd", "secret")
        if not hostname or not base_url or not username or not password:
            raise ValueError("Referential response must include hostname, api_url/base_url, login/username and password")
        return MasterServer(
            hostname=hostname,
            base_url=base_url,
            username=username,
            password=password,
            region=item.get("region") or "",
            locality=item.get("locality") or item.get("localite") or "",
            datacentre=item.get("datacentre") or item.get("datacenter") or "",
            is_baas=bool(item.get("is_baas", False)),
            is_raas=bool(item.get("is_raas", False)),
            domain_name=item.get("domain_name") or "",
            domain_type=item.get("domain_type") or "",
            raw=item,
        )


def split_hostnames(value: str) -> List[str]:
    return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]


def first(item: Dict[str, Any], *keys: str):
    for key in keys:
        if item.get(key) not in (None, ""):
            return item.get(key)
    return None


referential_service = ReferentialService()
