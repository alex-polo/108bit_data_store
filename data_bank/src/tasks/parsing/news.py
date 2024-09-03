import datetime
import logging
import traceback
from typing import Union, List

from sqlalchemy import select, CursorResult, insert

from src import Settings, NewsGatheringEvents, NewsGatheringSuccess
from src.config import get_browser_chrome_config, FormatPostParamsConfig
from src.database import get_session
from src.parsers import list_parsers
from src.tasks.celery import celery
from src.tasks.mics import registry_grubber_error
from src.tasks.parsing.loader import download
from src.tasks.parsing.news_adding_post import add_post
from src.tasks.parsing.news_parsing import parse
from src.tasks.parsing.news_post_editor import post_formation
from src.utils.classes import SuccessResponse, MalfunctionResponse, Status, ParsedData

logger = logging.getLogger()


def search_parser_function(parser_system_name: str):
    for parser in list_parsers:
        if parser.get('system_name') == parser_system_name:
            return parser.get('parser_func')


def get_settings_value(props: str) -> str:
    with get_session() as session:
        value = session.execute(select(Settings.value).where(Settings.name == props)).scalar()
        session.close()
    return value


def get_min_time_delta() -> int:
    return int(get_settings_value(props='news_number_of_days_to_view_sites'))


def get_format_post_params() -> FormatPostParamsConfig:
    return FormatPostParamsConfig(
        formatting_min_len_title=int(get_settings_value(props='news_formatting_min_len_title')),
        formatting_len_title=int(get_settings_value(props='news_formatting_len_title')),
        formatting_min_len_details=int(get_settings_value(props='news_formatting_min_len_details')),
        formatting_len_details=int(get_settings_value(props='news_formatting_len_details')),
        main_tag_news=get_settings_value(props='news_main_tag'),
        number_of_days_to_view_sites=int(get_settings_value(props='news_number_of_days_to_view_sites')),
        number_days_search_post=int(get_settings_value(props='news_number_days_search_post')),
        post_matcher_ratio=int(get_settings_value(props='news_post_matcher_ratio')),
        len_loaded_content=int(get_settings_value(props='news_len_loaded_content'))
    )


def create_success_event(news_site_id: int) -> None:
    with get_session() as session:
        cursor_event: CursorResult = session.execute(
            insert(NewsGatheringEvents).values(site_id=news_site_id, event='success_grubber', is_success=True)
        )
        session.execute(
            insert(NewsGatheringSuccess).values(event_id=cursor_event.inserted_primary_key[0],
                                                event='site_success_processed', details='')
        )
        session.commit()


@celery.task(name='news_site_task')
def news_site_task(news_site: dict):
    is_success: bool = True
    news_site_id = int(news_site.get('id'))
    news_site_name = news_site.get('name')
    try:
        news_site_vendor = news_site.get('vendor')
        news_site_field_tags = news_site.get('field_tags')
        news_site['parser_func'] = search_parser_function(news_site.get('parser_func'))
        browser_config = get_browser_chrome_config()
        min_time_delta = datetime.datetime.now() - datetime.timedelta(days=get_min_time_delta())
        max_time_delta = datetime.datetime.now() + datetime.timedelta(days=1)
        format_params: FormatPostParamsConfig = get_format_post_params()

        server_response: Union[SuccessResponse, MalfunctionResponse] = download(site=news_site,
                                                                                format_params=format_params,
                                                                                browser_config=browser_config)
        if server_response.status == Status.Ok:
            parser_response = parse(download_page_content=server_response.content,
                                    news_site=news_site,
                                    search_time=min_time_delta,
                                    browser_config=browser_config)
            for parser_response_item in parser_response:
                if parser_response_item.status == Status.Ok:
                    parser_data_list: List[ParsedData] = parser_response_item.content
                    for parser_data in parser_data_list:
                        if parser_data.is_valid:
                            # Выполняем проверку по дате
                            if min_time_delta <= parser_data.date < max_time_delta:
                                # Формируем пост
                                post_editor_response = post_formation(parsed_data=parser_data,
                                                                      site=news_site,
                                                                      format_params=format_params)
                                add_post(post_editor=post_editor_response,
                                         site=news_site,
                                         news_site_id=news_site_id,
                                         format_params=format_params,
                                         vendor_tag=news_site_vendor,
                                         field_tags=news_site_field_tags)

                            else:
                                logger.debug(f'Date out of range, {news_site_name}, parsed_data: {parser_data}')
                        else:
                            registry_grubber_error(news_site_id=news_site_id, error_response=parser_data.error_content)
                            is_success = False
                else:
                    registry_grubber_error(news_site_id=news_site_id, error_response=parser_response_item)
                    is_success = False
        else:
            registry_grubber_error(news_site_id=news_site_id, error_response=server_response)
            is_success = False

        if is_success:
            create_success_event(news_site_id=news_site_id)
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
                                   description=f'Текст ошибки:\n{str(error)}\nПодробнее в логе.',
                                   error_text=text_error,
                                   text_details=text_details))