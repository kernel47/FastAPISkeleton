from typing import Optional

from app.modules.netbackup.service import netbackup_service
from app.shared.odata import QueryOptions


class NetBackupController:
    async def list_policies(
        self,
        masters: Optional[str],
        limit: int,
        offset: int,
        filter_: Optional[str],
        raw: bool,
        policy_name: Optional[str],
        policy_type: Optional[str],
    ):
        return await netbackup_service.list_policies(
            masters,
            QueryOptions(limit=limit, offset=offset, filter=filter_, raw=raw),
            policy_name=policy_name,
            policy_type=policy_type,
        )

    async def get_policy(self, hostname: str, policy_name: str, raw: bool):
        return await netbackup_service.get_policy(hostname, policy_name, raw)

    async def list_jobs(
        self,
        masters: Optional[str],
        limit: int,
        offset: int,
        filter_: Optional[str],
        raw: bool,
        policy_name: Optional[str],
        client_name: Optional[str],
        status_code: Optional[int],
    ):
        return await netbackup_service.list_jobs(
            masters,
            QueryOptions(limit=limit, offset=offset, filter=filter_, raw=raw),
            policy_name=policy_name,
            client_name=client_name,
            status_code=status_code,
        )

    async def get_job(self, hostname: str, job_id: str, raw: bool):
        return await netbackup_service.get_job(hostname, job_id, raw)

    async def list_images(
        self,
        masters: Optional[str],
        limit: int,
        offset: int,
        filter_: Optional[str],
        raw: bool,
        policy_name: Optional[str],
        client_name: Optional[str],
    ):
        return await netbackup_service.list_images(
            masters,
            QueryOptions(limit=limit, offset=offset, filter=filter_, raw=raw),
            policy_name=policy_name,
            client_name=client_name,
        )

    async def get_image(self, hostname: str, image_id: str, raw: bool):
        return await netbackup_service.get_image(hostname, image_id, raw)


controller = NetBackupController()
