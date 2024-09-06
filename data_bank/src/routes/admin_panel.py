import logging
from typing import List

import fastapi
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.manager import current_active_user
from src.database import get_async_session
from src.models import (
    User,
    Parser,
    NewsGathering,
    CatalogsGathering)

from src.schemes import (
    ParsersResponse,
    ChangeParserQuery,
    NewsGatheringResponse,
    NewsGatheringQuery,
    NewsGatheringById,
    CatalogGatheringEntity,
    CatalogGatheringById
)

logger = logging.getLogger(__name__)

admin_panel_router = APIRouter(
    prefix='/admin-panel',
    tags=["admin-panel"],
)


@admin_panel_router.get("/get-news-parsers",
                        status_code=fastapi.status.HTTP_200_OK,
                        response_model=List[ParsersResponse])
async def get_news_parsers(session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    # return [ParsersResponse.model_validate(row, from_attributes=True)
    #         for row in (await session.execute(select(Parser).where(Parser.parser_type == 'news_parser')))
    #         .scalars().all()]

    list_parsers: List[ParsersResponse] = list()
    for row in (await session.execute(select(Parser).where(Parser.parser_type == 'news_parser'))).scalars().all():
        list_parsers.append(ParsersResponse(
            id=row.id,
            system_name=row.system_name,
            parser_name=row.parser_name,
            description=row.description,
            parser_type=row.parser_type,
            is_enable='Да' if row.is_enable else 'Нет',
            is_parser_scheme_missing='Отсутствует' if row.is_parser_scheme_missing else 'Активна',
        ))

    return list_parsers


@admin_panel_router.get("/get-catalog-parsers",
                        status_code=fastapi.status.HTTP_200_OK,
                        response_model=List[ParsersResponse])
async def get_catalog_parsers(session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    list_parsers: List[ParsersResponse] = list()
    for row in (await session.execute(select(Parser).where(Parser.parser_type == 'catalog_parser'))).scalars().all():
        list_parsers.append(ParsersResponse(
            id=row.id,
            system_name=row.system_name,
            parser_name=row.parser_name,
            description=row.description,
            parser_type=row.parser_type,
            is_enable='Да' if row.is_enable else 'Нет',
            is_parser_scheme_missing='Отсутствует' if row.is_parser_scheme_missing else 'Активна',
        ))

    return list_parsers


@admin_panel_router.get("/get-active-news-parsers",
                        status_code=fastapi.status.HTTP_200_OK,
                        response_model=List[ParsersResponse])
async def get_active_news_parsers(session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    list_parsers: List[ParsersResponse] = list()
    for row in (await session.execute(
            select(Parser).where(Parser.is_enable == True).where(
                Parser.is_parser_scheme_missing == False).where(Parser.parser_type == 'news_parser'))).scalars().all():
        list_parsers.append(ParsersResponse(
            id=row.id,
            system_name=row.system_name,
            parser_name=row.parser_name,
            description=row.description,
            parser_type=row.parser_type,
            is_enable='Да' if row.is_enable else 'Нет',
            is_parser_scheme_missing='Отсутствует' if row.is_parser_scheme_missing else 'Активна',
        ))

    return list_parsers


@admin_panel_router.get("/get-parser",
                        status_code=fastapi.status.HTTP_200_OK,
                        response_model=ParsersResponse)
async def get_parser(parser_system_name: str,
                     session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    parser = (await session.execute(select(Parser).where(Parser.system_name == parser_system_name))).scalar()
    return ParsersResponse(
        id=parser.id,
        system_name=parser.system_name,
        parser_name=parser.parser_name,
        description=parser.description,
        parser_type=parser.parser_type,
        is_enable='Да' if parser.is_enable else 'Нет',
        is_parser_scheme_missing='Отсутствует' if parser.is_parser_scheme_missing else 'Активна',
    )


@admin_panel_router.post("/save-change-parser",
                         status_code=fastapi.status.HTTP_202_ACCEPTED)
async def save_change_parser(value: ChangeParserQuery,
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN, detail="User is not superuser")

    await session.execute(update(Parser).where(Parser.system_name == value.system_name)
                          .values(parser_name=value.parser_name,
                                  description=value.description,
                                  is_enable=True if value.is_enable == 'Да' else False))
    await session.commit()


@admin_panel_router.get("/get-all-news-gathering",
                        status_code=fastapi.status.HTTP_200_OK,
                        response_model=List[NewsGatheringResponse])
async def get_all_news_gathering(session: AsyncSession = Depends(get_async_session),
                                 user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    list_news_entity: List[NewsGatheringResponse] = list()
    for row in (await session.execute(select(NewsGathering))).scalars().all():
        list_news_entity.append(NewsGatheringResponse(
            id=row.id,
            name=row.name,
            url=row.url,
            description=row.description,
            vendor=row.vendor,
            field_tags=row.field_tags,
            parser_id=row.parser_id,
            is_enable='Да' if row.is_enable else 'Нет'
        ))

    return list_news_entity


@admin_panel_router.post("/create-news-gathering",
                         status_code=fastapi.status.HTTP_201_CREATED)
async def create_news_gathering(data: NewsGatheringQuery, session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    await session.execute(insert(NewsGathering).values(name=data.name,
                                                       url=data.url,
                                                       description=data.description,
                                                       vendor=data.vendor,
                                                       field_tags=data.field_tags,
                                                       parser_id=data.parser_id,
                                                       is_enable=True if data.is_enable == 'Да' else False
                                                       ))

    await session.commit()


@admin_panel_router.post("/delete-news-gathering-by-id",
                         status_code=fastapi.status.HTTP_200_OK)
async def delete_news_gathering_by_id(data: NewsGatheringById, session: AsyncSession = Depends(get_async_session),
                                      user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    await session.execute(delete(NewsGathering).where(NewsGathering.id == data.id))
    await session.commit()


@admin_panel_router.get("/get-news-gathering-by-name",
                        status_code=fastapi.status.HTTP_200_OK,
                        response_model=NewsGatheringResponse)
async def get_news_gathering_by_name(name: str,
                                     session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    news_entity = (await session.execute(select(NewsGathering).where(NewsGathering.name == name))).scalar()
    return NewsGatheringResponse(
        id=news_entity.id,
        name=news_entity.name,
        url=news_entity.url,
        description=news_entity.description,
        vendor=news_entity.vendor,
        field_tags=news_entity.field_tags,
        parser_id=news_entity.parser_id,
        is_enable='Да' if news_entity.is_enable else 'Нет'
    )


@admin_panel_router.post("/update-news-entity",
                         status_code=fastapi.status.HTTP_202_ACCEPTED)
async def update_news_entity(data: NewsGatheringQuery,
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN, detail="User is not superuser")
    await session.execute(update(NewsGathering)
                          .where(NewsGathering.id == data.id)
                          .values(name=data.name,
                                  url=data.url,
                                  description=data.description,
                                  vendor=data.vendor,
                                  field_tags=data.field_tags,
                                  parser_id=data.parser_id,
                                  is_enable=True if data.is_enable == 'Да' else False
                                  ))
    await session.commit()


@admin_panel_router.get("/get-all-entity-catalogs-gathering",
                        status_code=fastapi.status.HTTP_200_OK,
                        response_model=List[CatalogGatheringEntity])
async def get_all_catalogs_gathering(session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    list_catalogs_entity: List[CatalogGatheringEntity] = list()
    for row in (await session.execute(select(CatalogsGathering))).scalars().all():
        list_catalogs_entity.append(CatalogGatheringEntity(
            id=row.id,
            name=row.name,
            url=row.url,
            description=row.description,
            parser_id=row.parser_id,
            is_enable='Да' if row.is_enable else 'Нет'
        ))

    return list_catalogs_entity


@admin_panel_router.post("/create-catalog-gathering",
                         status_code=fastapi.status.HTTP_201_CREATED)
async def create_catalog_gathering(data: CatalogGatheringEntity, session: AsyncSession = Depends(get_async_session),
                                   user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    await session.execute(insert(CatalogsGathering).values(name=data.name,
                                                           url=data.url,
                                                           description=data.description,
                                                           parser_id=data.parser_id,
                                                           is_enable=True if data.is_enable == 'Да' else False
                                                           ))

    await session.commit()


@admin_panel_router.post("/update-catalog-gathering",
                         status_code=fastapi.status.HTTP_202_ACCEPTED)
async def edit_catalog_gathering(data: CatalogGatheringEntity, session: AsyncSession = Depends(get_async_session),
                                 user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    await session.execute(update(CatalogsGathering)
                          .where(CatalogsGathering.id == data.id)
                          .values(name=data.name,
                                  url=data.url,
                                  description=data.description,
                                  parser_id=data.parser_id,
                                  is_enable=True if data.is_enable == 'Да' else False
                                  ))
    await session.commit()


@admin_panel_router.get("/get-catalog-gathering-by-name",
                        status_code=fastapi.status.HTTP_200_OK,
                        response_model=CatalogGatheringEntity)
async def get_catalog_gathering_by_name(name: str,
                                        session: AsyncSession = Depends(get_async_session),
                                        user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    catalog_entity = (await session.execute(select(CatalogsGathering).where(CatalogsGathering.name == name))).scalar()
    return CatalogGatheringEntity(
        id=catalog_entity.id,
        name=catalog_entity.name,
        url=catalog_entity.url,
        description=catalog_entity.description,
        parser_id=catalog_entity.parser_id,
        is_enable='Да' if catalog_entity.is_enable else 'Нет'
    )


@admin_panel_router.post("/delete-catalog-gathering-by-id",
                         status_code=fastapi.status.HTTP_200_OK)
async def delete_catalog_gathering_by_id(data: CatalogGatheringById,
                                         session: AsyncSession = Depends(get_async_session),
                                         user: User = Depends(current_active_user)):
    if user.is_superuser is False:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED)

    await session.execute(delete(CatalogsGathering).where(CatalogsGathering.id == data.id))
    await session.commit()
