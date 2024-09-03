import datetime
import difflib
import logging
from typing import Union

from sqlalchemy import select, insert, CursorResult

from src import NewsPosts, NewsGatheringEvents, NewsGathering, QueueOutputNewsPackage, NewsGatheringSuccess
from src.config import FormatPostParamsConfig
from src.database import get_session
from src.tasks.mics import registry_grubber_error
from src.utils.classes import PostData, SuccessResponse, MalfunctionResponse, Status

logger = logging.getLogger()


# def search_posts_in_database(new_post_title: str, new_post_details: str, db_posts_list, ratio: int) -> float:
#     """
#     Поиск поста в базе данных, если в постах из БД совпадает title или details возвращает True иначе False
#     :param new_post_title:
#     :param new_post_details:
#     :param db_posts_list:
#     :param ratio:
#     :return:
#     """
#     ratio = ratio * 0.01
#
#     for db_title, db_details in db_posts_list:
#         matcher_title = difflib.SequenceMatcher(None, new_post_title.lower(), db_title.lower()).ratio()
#         matcher_details = difflib.SequenceMatcher(None, new_post_details.lower(), db_details.lower()).ratio()
#
#         if matcher_title >= ratio and matcher_details >= ratio:
#             return True
#
#     return False


def search_posts(site_name: str, date: datetime):
    with get_session() as session:
        result = session.execute(
            select(NewsPosts.title, NewsPosts.details)
            .where((NewsPosts.date > date) & (NewsPosts.grubber_event_id == NewsGatheringEvents.id))
            .join(NewsGathering.grubber_events).filter(NewsGathering.name == site_name)
        )
        return result.fetchall()


def search_posts_in_database(new_post_title: str, new_post_details: str, db_posts_list, ratio: int) -> float:
    """
    Поиск поста в базе данных, если в постах из БД совпадает title или details возвращает True иначе False
    :param new_post_title:
    :param new_post_details:
    :param db_posts_list:
    :param ratio:
    :return:
    """
    ratio = ratio * 0.01

    for db_title, db_details in db_posts_list:
        matcher_title = difflib.SequenceMatcher(None, new_post_title.lower(), db_title.lower()).ratio()
        matcher_details = difflib.SequenceMatcher(None, new_post_details.lower(), db_details.lower()).ratio()

        if matcher_title >= ratio and matcher_details >= ratio:
            return True

    return False


def save_post_database(news_site_id: int, grubber_post: PostData):
    try:
        with get_session() as session:
            with session.begin():
                cursor_event: CursorResult = session.execute(
                    insert(NewsGatheringEvents).values(site_id=news_site_id, event='error_grubber', is_success=False)
                )
                cursor_post: CursorResult = session.execute(
                    insert(NewsPosts).values(date=grubber_post.date,
                                             title=grubber_post.title,
                                             details=grubber_post.details,
                                             more=grubber_post.more,
                                             image_url=grubber_post.image_url,
                                             main_tag=grubber_post.main_tag,
                                             field_tags=grubber_post.fields_tags,
                                             author=grubber_post.author,
                                             grubber_event_id=
                                             cursor_event.inserted_primary_key[0],
                                             owner='grubber')
                )
                session.execute(
                    insert(QueueOutputNewsPackage).values(post_id=cursor_post.inserted_primary_key[0], status='send')
                )

                session.commit()
    except:
        session.rollback()
        raise


def add_post(post_editor: Union[SuccessResponse, MalfunctionResponse],
             site: dict,
             news_site_id: int,
             format_params: FormatPostParamsConfig,
             vendor_tag: str,
             field_tags: str) -> None:
    """
    Функция выполняет проверку существует ли переднный пост в базе данных, если его нет создает событие и
    вносит его в базу данных
    :return:
    """
    if post_editor.status == Status.Ok:
        post: PostData = post_editor.content

        post.main_tag = format_params.main_tag_news
        post.fields_tags = field_tags
        post.author = vendor_tag

        search_time = datetime.datetime.now() - datetime.timedelta(format_params.number_days_search_post)
        # Выполняем поиск существующих постов по вендору за последних number_days_search_post из settings.py

        db_posts = search_posts(site_name=site.get('name'), date=search_time)

        # Делаем проверку есть ли пост уже в базе данных
        logger.debug(f'Checking if the post is already in the database: {post}')
        if not search_posts_in_database(new_post_title=post.title, new_post_details=post.details,
                                        db_posts_list=db_posts, ratio=format_params.post_matcher_ratio):

            logger.debug(f'Add post to database: {post}')
            # Создаем событие граббера в базе данных
            # event_id = registry_grubber_event(db_engine=_DB_ENGINE, site_id=news_site_id), event_description='adding_post_to_the_database', is_success=True)

            # Добавляем пост в базу данных
            save_post_database(news_site_id=news_site_id, grubber_post=post)

            # Если в процессе формирования поста были недочеты вносим их в БД
            # for malfunction in post.malfunctions:
            #     print(malfunction)
            #     registry_grubber_error(news_site_id=news_site_id, error_response=malfunction)
        else:
            logger.debug(f'The news is already in the database, parsed data: {post}')
    else:
        pass
        # event_id = db_query.registry_grubber_event(db_engine=_DB_ENGINE, site_id=news_site_id,
        #                                            event_description='error_adding_post_to_the_database',
        #                                            is_success=False)
        # registry_grubber_error(news_site_id=news_site_id, error_response=post_editor)
