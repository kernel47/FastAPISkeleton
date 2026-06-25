from typing import Optional

from app.modules.netbackup.service import netbackup_service


class MasterServerController:
    async def list_master_servers(
        self,
        region: Optional[str],
        locality: Optional[str],
        datacentre: Optional[str],
        is_baas: Optional[bool],
        is_raas: Optional[bool],
    ):
        return await netbackup_service.list_master_servers(
            region=region,
            locality=locality,
            datacentre=datacentre,
            is_baas=is_baas,
            is_raas=is_raas,
        )

    async def get_master_server(self, hostname: str):
        return await netbackup_service.get_master_server(hostname)


controller = MasterServerController()
