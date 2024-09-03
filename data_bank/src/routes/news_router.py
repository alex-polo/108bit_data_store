import logging
from random import randrange

import fastapi
from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src import User, NewsPosts, QueueOutputNewsPackage, Settings
from src.auth.manager import current_active_user
from src.database import get_async_session
from src.schemes import NewsPost, UpdatePostRequest

logger = logging.getLogger(__name__)

news_bot_router = APIRouter(
    prefix='/news-bot',
    tags=["news-bot"],
)


@news_bot_router.get("/get-news-post",
                     status_code=fastapi.status.HTTP_200_OK,
                     response_model=NewsPost)
async def get_news_post(session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_active_user)):
    # list_parsers: List[ParsersResponse] = list()
    queue_post_id = (await session.execute(
        select(QueueOutputNewsPackage.post_id)
        .where(QueueOutputNewsPackage.status == 'send')
        .order_by(QueueOutputNewsPackage.created_on).limit(1)
    )).scalar()

    post = (await session.execute(
        select(NewsPosts).where(NewsPosts.id == queue_post_id)
    )).scalar()

    return NewsPost(
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


@news_bot_router.get("/update-status-news-post",
                     status_code=fastapi.status.HTTP_202_ACCEPTED,
                     response_model=None)
async def update_status_news_post(id: int, session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_active_user)):
    await session.execute(
        update(QueueOutputNewsPackage)
        .where(QueueOutputNewsPackage.post_id == id).values(status='archive')
    )
    await session.commit()


@news_bot_router.get("/get-send-time",
                     status_code=fastapi.status.HTTP_200_OK,
                     response_model=int)
async def update_status_news_post(session: AsyncSession = Depends(get_async_session),
                                  # user: User = Depends(current_active_user)
                                  ):
    settings = (
            await session.execute(
                select(Settings.value).where(Settings.name.in_(['news_bot_min_time', 'news_bot_max_time']))
            )).scalars().all()

    return randrange(start=int(settings[0]), stop=int(settings[1]))
