from typing import Any, Callable, Dict, List, Optional, Tuple

import httpx

from app.core.config import settings
from app.modules.netbackup.client import NetBackupClient
from app.modules.netbackup.parser import parse_image, parse_job, parse_policy
from app.modules.referential.models import MasterServer
from app.modules.referential.service import referential_service
from app.shared.odata import QueryOptions, combine_odata, netbackup_cursor_params, netbackup_page_params, simple_filters_to_odata
from app.shared.parser import extract_items, extract_next_after, extract_total
from app.shared.response import Page


class NetBackupService:
    async def list_master_servers(self, **filters) -> List[MasterServer]:
        return await referential_service.list_master_servers(**filters)

    async def get_master_server(self, hostname: str) -> MasterServer:
        return await referential_service.get_master_server(hostname)

    async def list_policies(
        self,
        masters: Optional[str],
        options: QueryOptions,
        policy_name: Optional[str] = None,
        policy_type: Optional[str] = None,
    ) -> Page:
        simple_filter = simple_filters_to_odata({"policy_name": policy_name, "policy_type": policy_type})
        odata_filter = combine_odata(options.filter, simple_filter)
        return await self._collect_offset(
            masters,
            settings.netbackup_policies_path,
            parse_policy,
            options,
            odata_filter,
        )

    async def get_policy(self, hostname: str, policy_name: str, raw: bool = False) -> Dict[str, Any]:
        master = await referential_service.get_master_server(hostname)
        payload = await self._get(master, settings.netbackup_policy_detail_path.format(policy_name=policy_name))
        item = first_item(payload)
        parsed = parse_policy(item, raw=raw)
        parsed["master_server"] = master.hostname
        return parsed

    async def list_jobs(
        self,
        masters: Optional[str],
        options: QueryOptions,
        policy_name: Optional[str] = None,
        client_name: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> Page:
        simple_filter = simple_filters_to_odata(
            {"policy_name": policy_name, "client_name": client_name, "status_code": status_code}
        )
        odata_filter = combine_odata(options.filter, simple_filter)
        return await self._collect_cursor(
            masters,
            settings.netbackup_jobs_path,
            parse_job,
            options,
            odata_filter,
        )

    async def get_job(self, hostname: str, job_id: str, raw: bool = False) -> Dict[str, Any]:
        master = await referential_service.get_master_server(hostname)
        payload = await self._get(master, settings.netbackup_job_detail_path.format(job_id=job_id))
        item = first_item(payload)
        parsed = parse_job(item, raw=raw)
        parsed["master_server"] = master.hostname
        return parsed

    async def list_images(
        self,
        masters: Optional[str],
        options: QueryOptions,
        policy_name: Optional[str] = None,
        client_name: Optional[str] = None,
    ) -> Page:
        simple_filter = simple_filters_to_odata({"policy_name": policy_name, "client_name": client_name})
        odata_filter = combine_odata(options.filter, simple_filter)
        return await self._collect_cursor(
            masters,
            settings.netbackup_images_path,
            parse_image,
            options,
            odata_filter,
        )

    async def get_image(self, hostname: str, image_id: str, raw: bool = False) -> Dict[str, Any]:
        master = await referential_service.get_master_server(hostname)
        payload = await self._get(master, settings.netbackup_image_detail_path.format(image_id=image_id))
        item = first_item(payload)
        parsed = parse_image(item, raw=raw)
        parsed["master_server"] = master.hostname
        return parsed

    async def _collect_offset(
        self,
        masters: Optional[str],
        path: str,
        parser: Callable[[Dict[str, Any], bool], Dict[str, Any]],
        options: QueryOptions,
        odata_filter: Optional[str],
    ) -> Page:
        rows = []
        total = 0
        for master in await referential_service.resolve_many(masters):
            params = netbackup_page_params(options.limit, options.offset, odata_filter)
            payload = await self._get(master, path, params=params)
            rows.extend(self._parse_items(master, payload, parser, options.raw))
            total += extract_total(payload, 0)
        return Page(items=rows[: options.limit], total=total or len(rows), limit=options.limit, offset=options.offset)

    async def _collect_cursor(
        self,
        masters: Optional[str],
        path: str,
        parser: Callable[[Dict[str, Any], bool], Dict[str, Any]],
        options: QueryOptions,
        odata_filter: Optional[str],
    ) -> Page:
        rows = []
        for master in await referential_service.resolve_many(masters):
            rows.extend(await self._cursor_for_master(master, path, parser, options, odata_filter))
        return Page(items=rows[: options.limit], total=len(rows), limit=options.limit, offset=options.offset)

    async def _cursor_for_master(
        self,
        master: MasterServer,
        path: str,
        parser: Callable[[Dict[str, Any], bool], Dict[str, Any]],
        options: QueryOptions,
        odata_filter: Optional[str],
    ) -> List[Dict[str, Any]]:
        rows = []
        after = None
        skipped = 0
        page_size = min(settings.netbackup_default_page_size, options.limit)
        while len(rows) < options.limit:
            params = netbackup_cursor_params(page_size, after, odata_filter)
            try:
                payload = await self._get(master, path, params=params)
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    break
                raise
            items = extract_items(payload)
            if not items:
                break
            parsed = self._parse_items(master, payload, parser, options.raw)
            for item in parsed:
                if skipped < options.offset:
                    skipped += 1
                    continue
                rows.append(item)
                if len(rows) >= options.limit:
                    break
            after = extract_next_after(payload)
            if not after:
                break
        return rows

    async def _get(self, master: MasterServer, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        client = NetBackupClient(master)
        token = await client.login()
        return await client.get(path, token, params=params)

    def _parse_items(self, master: MasterServer, payload: Any, parser, raw: bool) -> List[Dict[str, Any]]:
        items = []
        for item in extract_items(payload):
            parsed = parser(item, raw=raw)
            parsed["master_server"] = master.hostname
            items.append(parsed)
        return items


def first_item(payload: Any) -> Dict[str, Any]:
    items = extract_items(payload)
    if not items:
        raise ValueError("Resource not found")
    return items[0]


netbackup_service = NetBackupService()
