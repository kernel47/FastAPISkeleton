from typing import Optional

from fastapi import APIRouter, Query

from app.api.controllers.master_servers import controller

router = APIRouter()


@router.get("")
async def list_master_servers(
    region: Optional[str] = None,
    locality: Optional[str] = None,
    datacentre: Optional[str] = None,
    is_baas: Optional[bool] = Query(None),
    is_raas: Optional[bool] = Query(None),
):
    return await controller.list_master_servers(region, locality, datacentre, is_baas, is_raas)


@router.get("/{hostname}")
async def get_master_server(hostname: str):
    return await controller.get_master_server(hostname)
