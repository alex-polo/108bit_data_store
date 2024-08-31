import logging
from typing import List

import fastapi
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src import User, Parser, NewsGathering
from src.auth.manager import current_active_user
from src.database import get_async_session
from src.schemes import ParsersResponse, ChangeParserQuery, NewsGatheringResponse

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

    # list_parsers: list = [ParsersResponse.model_validate(row, from_attributes=True)
    #                       for row in
    #                       (await session.execute(select(Parser).where(Parser.parser_type == 'catalog_parser')))
    #                       .scalars().all()]

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

    print((await session.execute(select(Parser).where(Parser.system_name == value.system_name))).scalar())
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
            description=row.description,
            vendor=row.vendor,
            field_tags=row.field_tags,
            parser_id=row.parser_id,
            is_enable='Да' if row.is_enable else 'Нет'
        ))

    return list_news_entity

#
#         await session.commit()
#     except IntegrityError as error:
#         print(error)
#         raise HTTPException(status_code=fastapi.status.HTTP_409_CONFLICT, detail="Organization already exists")
#     except Exception as error:
#         print(error)
#         raise HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error server")


# @frontend_router.post("/update-organization",
#                       status_code=fastapi.status.HTTP_200_OK)
# async def update_organization(value: OrganizationResponse,
#                               session: AsyncSession = Depends(get_async_session),
#                               user: User = Depends(current_active_user)):
#     if user.is_superuser is False:
#         raise HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN)
#     try:
#         await session.execute(update(Organization).values(name=value.name,
#                                                           short_name=value.short_name,
#                                                           address=value.address,
#                                                           inn=value.inn,
#                                                           supervisor=value.supervisor,
#                                                           description=value.description,
#                                                           is_active=value.is_active).filter_by(id=value.id))
#         await session.commit()
#     except IntegrityError as error:
#         print(error)
#         raise HTTPException(status_code=fastapi.status.HTTP_409_CONFLICT)
#     except Exception as error:
#         print(error)
#
#
# @frontend_router.get("/get-organization",
#                      status_code=fastapi.status.HTTP_200_OK, response_model=List[UserOrganizationsResponse])
# async def get_organization(session: AsyncSession = Depends(get_async_session),
#                            user: User = Depends(current_active_user)):
#     if user.is_superuser is False:
#         raise HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN)
#
#     user_organizations_response = list()
#     for organization_id, role_id in (await session.execute(
#             select(UserOrganization.organization_id,
#                    UserOrganization.role_id).where(UserOrganization.user_id == user.id))).all():
#         user_organizations_response.append(
#             UserOrganizationsResponse(
#                 organization=OrganizationResponse.model_validate(
#                     (await session.execute(select(Organization).where(Organization.id == organization_id))).scalar(),
#                     from_attributes=True),
#                 role=(await session.execute(
#                     select(OrganizationUserRole.role_name).where(OrganizationUserRole.id == role_id))).scalar()
#             )
#         )
#
#     return user_organizations_response
#
#
# @frontend_router.post("/create-object",
#                       status_code=fastapi.status.HTTP_201_CREATED)
# async def create_object(value: CreateObjectQuery,
#                         session: AsyncSession = Depends(get_async_session),
#                         user: User = Depends(current_active_user)):
#     # if user.is_superuser is False:
#     #     raise HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN)
#     try:
#         await session.execute(insert(Object).values(name=value.name, description=value.description))
#         await session.commit()
#     except IntegrityError as error:
#         print(error)
#         raise HTTPException(status_code=fastapi.status.HTTP_409_CONFLICT)
#     except Exception as error:
#         print(error)
#
#
# @frontend_router.get("/get-objects",
#                      status_code=fastapi.status.HTTP_200_OK, response_model=List[ObjectResponse])
# async def get_objects(session: AsyncSession = Depends(get_async_session),
#                       user: User = Depends(current_active_user)):
#     if user.is_superuser is False:
#         raise HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN)
#
#     return [ObjectResponse.model_validate(row, from_attributes=True)
#             for row in (await session.execute(select(Object))).scalars().all()]
#
#
# @frontend_router.get("/get-all-users",
#                      status_code=fastapi.status.HTTP_200_OK, response_model=List[UserRead])
# async def get_all_users(session: AsyncSession = Depends(get_async_session),
#                         # user: User = Depends(current_active_user)
#                         ):
#     # if user.is_superuser is False:
#     #     raise HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN)
#
#     user_list = [UserRead.model_validate(row, from_attributes=True)
#                  for row in (await session.execute(select(User))).scalars().all()]
#     new_user_list = list()
#     for _ in range(0, 1000):
#         new_user_list.append(user_list[0])
#         new_user_list.append(user_list[1])
#     return new_user_list
