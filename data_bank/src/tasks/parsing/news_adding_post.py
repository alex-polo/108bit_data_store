import datetime
import difflib
import logging
from typing import Union

from src.tasks.parsing.news import registry_grubber_error
from src.utils.classes import PostData, SuccessResponse, MalfunctionResponse, Status

logger = logging.getLogger()


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


async def add_post(post_editor: Union[SuccessResponse, MalfunctionResponse],
                   # site: dict,
                   news_site_id: int,
                   search_time: datetime, main_tag: str, vendor_tag: str, field_tags: str) -> None:
    """
    Функция выполняет проверку существует ли переднный пост в базе данных, если его нет создает событие и
    вносит его в базу данных
    :return:
    """
    if post_editor.status == Status.Ok:
        post: PostData = post_editor.content

        # post.main_tag = main_tag
        # post.fields_tags = field_tags
        # post.author = vendor_tag
        """
        news_site_processing_timeout: int = 108 * 14
#
        # Максимальное количество дней за которое осуществляется поиск новостей
        number_of_days_to_view_sites: int = 3
        # Максимальное количество дней учитываемых при поиске постов в базе данных, для сравнения с новой новостью
        number_days_search_post: int = 870
       # Процент совпадения title или details при сравнивании постов с базой данных, указывается значение от 0 до 100
        post_matcher_ratio: int = 97
        """

        search_time = datetime.datetime.now() - datetime.timedelta(number_days_search_post)
        # Выполняем поиск существующих постов по вендору за последних number_days_search_post из settings.py
        db_posts = db_query.search_posts(db_engine=_DB_ENGINE, site_name=site.get('site_name'), date=search_time)

        # Делаем проверку есть ли пост уже в базе данных
        logger.debug(f'Checking if the post is already in the database: {post}')
        if not search_posts_in_database(new_post_title=post.title, new_post_details=post.details,
                                        db_posts_list=db_posts, ratio=post_matcher_ratio):

            logger.debug(f'Add post to database: {post}')
            # Создаем событие граббера в базе данных
            # event_id = registry_grubber_event(db_engine=_DB_ENGINE, site_id=news_site_id), event_description='adding_post_to_the_database', is_success=True)

            # Добавляем пост в базу данных
            db_query.add_grubber_post(db_engine=_DB_ENGINE, event_id=event_id, grubber_post=post)

            # Если в процессе формирования поста были недочеты вносим их в БД
            for malfunction in post.malfunctions:
                registry_grubber_error(news_site_id=news_site_id, error_response=malfunction)
        else:
            logger.debug(f'The news is already in the database, parsed data: {post}')
    else:
        event_id = db_query.registry_grubber_event(db_engine=_DB_ENGINE, site_id=news_site_id, event_description='error_adding_post_to_the_database', is_success=False)
        registry_grubber_error(news_site_id=news_site_id, error_response=post_editor)
