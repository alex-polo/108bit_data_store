from typing import List

from sqlalchemy import select

from .celery import celery
from src.models import NewsGathering
from src.database import get_session
from .parsing.news import news_site_task


@celery.task(name='sheduler_news_task')
def task_scheduler():
    # list_news_entity: List[NewsSiteEntity] = list()
    list_news_entity: List[dict] = list()
    with (get_session() as session):
        for news_site in session.execute(
                select(NewsGathering).where(NewsGathering.is_enable.is_(True))
        ).scalars().all():
            list_news_entity.append(
                {
                    'id': news_site.id,
                    'name': news_site.name,
                    'url': news_site.url,
                    'vendor': news_site.vendor,
                    'field_tags': news_site.field_tags,
                    'parser_func': news_site.parser.system_name,
                }
            )

    for news_site in list_news_entity:
        news_site_task.delay(news_site)
