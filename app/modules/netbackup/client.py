from typing import Any, Dict, Optional

from app.core.config import settings
from app.modules.referential.models import MasterServer
from app.shared.http import HttpClient


class NetBackupClient:
    def __init__(self, master: MasterServer):
        self.master = master
        self.http = HttpClient(master.base_url)

    async def login(self) -> str:
        payload = {"userName": self.master.username, "password": self.master.password}
        if self.master.domain_name:
            payload["domainName"] = self.master.domain_name
        if self.master.domain_type:
            payload["domainType"] = self.master.domain_type
        response = await self.http.post(settings.netbackup_login_path, json=payload)
        token = self._extract_token(response)
        if not token:
            raise ValueError("NetBackup login response does not contain token")
        return token

    async def get(self, path: str, token: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self.http.get(path, headers=self._headers(token), params=params)

    def _headers(self, token: str) -> Dict[str, str]:
        value = token
        if settings.netbackup_token_prefix:
            value = "%s %s" % (settings.netbackup_token_prefix, token)
        return {settings.netbackup_token_header: value, "Accept": "application/json"}

    def _extract_token(self, payload: Any):
        if not isinstance(payload, dict):
            return None
        if payload.get("token"):
            return payload.get("token")
        if payload.get("access_token"):
            return payload.get("access_token")
        data = payload.get("data") or {}
        attributes = data.get("attributes") if isinstance(data, dict) else {}
        if isinstance(attributes, dict):
            return attributes.get("token") or attributes.get("access_token")
        return None
