from fastapi import APIRouter

from .internet_sites import internet_sites_router

admin_panel_router = APIRouter(
    prefix='/admin-panel',
    tags=["admin-panel"],
)

admin_panel_router.include_router(internet_sites_router)