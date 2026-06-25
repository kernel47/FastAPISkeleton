from typing import Optional

from fastapi import APIRouter, Query

from app.api.controllers.netbackup import controller
from app.shared.response import Page

router = APIRouter()


@router.get("/policies", response_model=Page)
async def list_policies(
    masters: Optional[str] = Query(None, description="Comma separated master-server hostnames. Empty means all."),
    policy_name: Optional[str] = Query(None, description="Simple filter converted to OData policyName."),
    policy_type: Optional[str] = Query(None, description="Simple filter converted to OData policyType."),
    filter_: Optional[str] = Query(None, alias="$filter", description="Raw OData filter sent to NetBackup."),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    raw: bool = Query(False),
):
    return await controller.list_policies(masters, limit, offset, filter_, raw, policy_name, policy_type)


@router.get("/policies/{policy_name}")
async def get_policy(hostname: str, policy_name: str, raw: bool = False):
    return await controller.get_policy(hostname, policy_name, raw)


@router.get("/jobs", response_model=Page)
async def list_jobs(
    masters: Optional[str] = Query(None, description="Comma separated master-server hostnames. Empty means all."),
    policy_name: Optional[str] = None,
    client_name: Optional[str] = None,
    status_code: Optional[int] = None,
    filter_: Optional[str] = Query(None, alias="$filter"),
    limit: int = Query(100, ge=1, le=5000),
    offset: int = Query(0, ge=0),
    raw: bool = Query(False),
):
    return await controller.list_jobs(masters, limit, offset, filter_, raw, policy_name, client_name, status_code)


@router.get("/jobs/{job_id}")
async def get_job(hostname: str, job_id: str, raw: bool = False):
    return await controller.get_job(hostname, job_id, raw)


@router.get("/images", response_model=Page)
async def list_images(
    masters: Optional[str] = Query(None, description="Comma separated master-server hostnames. Empty means all."),
    policy_name: Optional[str] = None,
    client_name: Optional[str] = None,
    filter_: Optional[str] = Query(None, alias="$filter"),
    limit: int = Query(100, ge=1, le=5000),
    offset: int = Query(0, ge=0),
    raw: bool = Query(False),
):
    return await controller.list_images(masters, limit, offset, filter_, raw, policy_name, client_name)


@router.get("/images/{image_id}")
async def get_image(hostname: str, image_id: str, raw: bool = False):
    return await controller.get_image(hostname, image_id, raw)
