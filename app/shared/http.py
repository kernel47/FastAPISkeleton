from typing import Any, Dict, Optional

import httpx

from app.core.config import settings


class HttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = "%s/%s" % (self.base_url, path.lstrip("/"))
        timeout = httpx.Timeout(settings.http_timeout_seconds)
        async with httpx.AsyncClient(timeout=timeout, verify=settings.http_verify_tls) as client:
            response = await client.request(method, url, headers=headers, params=params, json=json)
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            return response.json()

    async def get(self, path: str, headers=None, params=None) -> Any:
        return await self.request("GET", path, headers=headers, params=params)

    async def post(self, path: str, headers=None, json=None) -> Any:
        return await self.request("POST", path, headers=headers, json=json)
