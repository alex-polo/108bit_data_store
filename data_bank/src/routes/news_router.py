import logging
from http.client import HTTPException
from random import randrange

import fastapi
from fastapi import APIRouter, Depends
from sqlalchemy import select, update, desc
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.auth.manager import current_active_user
from src.database import get_async_session

from src.schemes import (
    NewsPostScheme,
    DispatchTimeScheme, UpdatePostScheme, TgUserScheme
)

from src.models import (
    User,
    NewsPosts,
    QueueOutputNewsPackage,
    Settings,
    TgUser
)

logger = logging.getLogger(__name__)

news_bot_router = APIRouter(
    prefix='/news-bot',
    tags=["news-bot"],
)


@news_bot_router.get("/get-news-post",
                     responses={
                         fastapi.status.HTTP_200_OK:
                                    {'model': NewsPostScheme,
                                    'description': 'Success response',},
                         fastapi.status.HTTP_204_NO_CONTENT:
                                    {'model': {},
                                    'description': 'No content response',},
                         fastapi.status.HTTP_403_FORBIDDEN:
                                    {'model': str,
                                    'description': 'User does not have permissions'}})
async def get_news_post(session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_active_user)):
    if user.is_news_bot is False:
        raise HTTPException(fastapi.status.HTTP_403_FORBIDDEN, 'User does not have permissions')

    post = (await session.execute(
        select(NewsPosts)
        .join(QueueOutputNewsPackage, NewsPosts.id == QueueOutputNewsPackage.post_id)
        .where(QueueOutputNewsPackage.status == 'send')
        .order_by(desc(QueueOutputNewsPackage.created_on)).limit(1)
    )).scalar()

    if post is not None:
        return NewsPostScheme(
            id=post.id,
            date=post.date.timestamp(),
            title=post.title,
            details=post.details,
            more=post.more,
            image_url=post.image_url,
            main_tag=post.main_tag,
            field_tags=post.field_tags,
            vendor=post.author
        )
    else:
        return Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)



@news_bot_router.post("/update-status-news-post",
                     responses={
                                fastapi.status.HTTP_202_ACCEPTED:
                                    {'model': None,
                                    'description': 'Success response',},
                                fastapi.status.HTTP_403_FORBIDDEN:
                                    {'model': str,
                                    'description': 'User does not have permissions'}})

async def update_status_news_post(data: UpdatePostScheme, session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_active_user)):
    if user.is_news_bot is False:
        raise HTTPException(fastapi.status.HTTP_403_FORBIDDEN, 'User does not have permissions')

    await session.execute(
        update(QueueOutputNewsPackage)
        .where(QueueOutputNewsPackage.post_id == data.post_id).values(status='archive')
    )
    await session.commit()



@news_bot_router.get("/get-dispatch-time",
                     responses={
                         fastapi.status.HTTP_200_OK:
                             {'model': DispatchTimeScheme,
                              'description': 'Success response', },
                         fastapi.status.HTTP_403_FORBIDDEN:
                             {'model': str,
                              'description': 'User does not have permissions'}})
async def update_status_news_post(session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_active_user)):
    if user.is_news_bot is False:
        raise HTTPException(fastapi.status.HTTP_403_FORBIDDEN, 'User does not have permissions')

    settings = (
            await session.execute(
                select(Settings.value).where(Settings.name.in_(['news_bot_min_time', 'news_bot_max_time']))
            )).scalars().all()

    return DispatchTimeScheme(time=randrange(start=int(settings[0]), stop=int(settings[1])))



@news_bot_router.get("/update-telegram-users",
                     status_code=fastapi.status.HTTP_202_ACCEPTED,
                     response_model=None)
async def update_news_bot_telegram_users(data: TgUserScheme, session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_active_user)):
    tg_user = (await session.execute(select(TgUser).where(TgUser.tg_identifier == data.tg_identifier))).scalar()
    if tg_user is None:
        await session.execute(
            insert(TgUser).values(
                tg_identifier=data.tg_identifier,
                tg_bot='',
                first_name=data.first_name,
                second_name=data.second_name,
                surname=data.surname,
                phone_number_tg: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
        is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=True)
        update_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now,
                                                    onupdate=datetime.now())
        created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now)
            )
        )
    else:
        await session.execute(
        update(TgUser)
        .where(TgUser.tg_id == data.tg_identifier).values(status='archive'))

    await session.commit()


@news_bot_router.post("/update-news-bot-telegram-users",
                     status_code=fastapi.status.HTTP_202_ACCEPTED)
async def update_news_bot_telegram_users(tg_identifier: int,
                           session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_active_user)):
    tg_user = (await session.execute(select(TgUser).where(TgUser.tg_id == tg_identifier))).scalar()
    with session.begin():
        if tg_user is None:
            await session.execute(
                insert(TgUser).values()
            )


