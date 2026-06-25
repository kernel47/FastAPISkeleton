from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.master_servers import router as master_servers_router
from app.api.routes.netbackup import router as netbackup_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(master_servers_router, prefix="/master-servers", tags=["master-servers"])
router.include_router(netbackup_router, prefix="/netbackup", tags=["netbackup"])
