import fastapi
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, InternetSite
from src.auth.manager import current_active_user
from src.database import get_async_session
from src.schemes import InternetSiteDTO

internet_sites_router = APIRouter(
    prefix='/internet-sites',
    tags=['admin-panel'],
)


@internet_sites_router.get("/get-all-sites",
                           responses={
                            fastapi.status.HTTP_200_OK:
                                    {'model': InternetSiteDTO,
                                    'description': 'Success response',},
                            fastapi.status.HTTP_403_FORBIDDEN:
                                    {'model': str,
                                    'description': 'User does not have permissions'}})
async def get_internet_sites(session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    return [InternetSiteDTO.model_validate(row, from_attributes=True)
            for row in (await session.execute(select(InternetSite))).scalars().all()]