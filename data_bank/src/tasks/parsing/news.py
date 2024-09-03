import datetime
import logging
import traceback
from typing import Union

from sqlalchemy import insert, CursorResult, Row

from src import NewsGatheringEvents, NewsGatheringMalfunctions
from src.config import get_browser_chrome_config
from src.database import get_session
from src.parsers import list_parsers
from src.tasks.celery import celery
from src.tasks.parsing.loader import download
from src.utils.classes import SuccessResponse, MalfunctionResponse, Status

logger = logging.getLogger()


def search_parser_function(parser_system_name: str):
    for parser in list_parsers:
        if parser.get('system_name') == parser_system_name:
            return parser.get('parser_func')


def registry_grubber_error(news_site_id: int, error_response: MalfunctionResponse) -> None:
    with get_session() as session:
        try:
            cursor: CursorResult = session.execute(
                    insert(NewsGatheringEvents).values(site_id=news_site_id, event='error_grubber', is_success=False)
                )
            print(cursor.inserted_primary_key[0])
            session.execute(
                    insert(NewsGatheringMalfunctions).values(
                        event_id=cursor.inserted_primary_key[0],
                        malfunction_type=error_response.type,
                        malfunction_details=error_response.type_detail,
                        service_name=error_response.service_name,
                        module_name=error_response.module_name,
                        source=error_response.source,
                        date=error_response.date,
                        title=error_response.title,
                        description=error_response.description,
                        text_error=error_response.error_text,
                        text_details=error_response.text_details,
                        attribute_1=error_response.attribute_1,
                        attribute_2=error_response.attribute_2,
                        attribute_3=error_response.attribute_3,
                        attribute_4=error_response.attribute_4,
                        attribute_5=error_response.attribute_5
                    )
                )

            session.commit()
        except Exception as error:
            logger.error(error)
            session.rollback()
        finally:
            session.close()


@celery.task(name='news_site_task')
def news_site_task(news_site: dict):
    news_site_id = int(news_site.get('id'))
    news_site_name = news_site.get('name')
    news_site_url = news_site.get('url')
    news_site_vendor = news_site.get('vendor')
    news_site_field_tags = news_site.get('field_tags').split(',')
    news_site_parser_func = search_parser_function(news_site.get('parser_func'))
    browser_config = get_browser_chrome_config()
    # Берем из базы данных
    # min_time_delta = datetime.datetime.now() - datetime.timedelta(days=grubber_config.number_of_days_to_view_sites)
    # max_time_delta = datetime.datetime.now() + datetime.timedelta(days=1)

    search_time = None

    try:
        server_response: Union[SuccessResponse, MalfunctionResponse] = download(site=news_site,
                                                                                browser_config=browser_config)
        if server_response.status == Status.Ok:
            print('Успех')
        else:
            registry_grubber_error(news_site_id=news_site_id, error_response=server_response)

    except Exception as error:
        text_error = 'News site task непредвиденная ошибка ' + str(error)
        logger.error(text_error)
        text_details = traceback.format_exc(limit=None, chain=True)
        logger.error(text_details)

        registry_grubber_error(news_site_id=news_site_id,
                               error_response=MalfunctionResponse(
                                   status=Status.Error,
                                   date=datetime.datetime.now(),
                                   type='error',
                                   type_detail='grubber_error',
                                   service_name='grubber_service',
                                   module_name='site_processing_event',
                                   source=news_site_name,
                                   title='Grubber loop непредвиденная ошибка',
                                   description=f'Текст ошибки:\n{str(error)}'
                                               f'\nПодробнее в логе.',
                                   error_text=text_error,
                                   text_details=text_details))

    # Скачиваем данные

    # if downloaded_page is not None:
    #     news_site_parser_func(page_body=downloaded_page,
    #                           # search_time: datetime,
    #                           browser_config=browser_config,
    #                           site={'site': news_site_name, 'url': news_site_url})

    # async def wirenboard_parser(page_body: str,
    #                             search_time: datetime,
    #                             browser_config: BrowserChromeConfig,
    #                             site) -> List[ParsedData]:
