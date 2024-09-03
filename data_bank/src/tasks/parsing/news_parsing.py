import datetime
import logging
import traceback
from typing import List, Union, Optional

import aiohttp
import requests

from src.config import BrowserChromeConfig
from src.utils.classes import SuccessResponse, MalfunctionResponse, ParsedData, Status

logger = logging.getLogger()


def parsing_error_response(site: dict, description: Optional[str], error_text: Optional[str],
                           text_details: Optional[str],
                           url: Optional[str]) -> MalfunctionResponse:
    return MalfunctionResponse(status=Status.Error,
                               date=datetime.datetime.now(),
                               type='error',
                               type_detail='parsing_error',
                               service_name='grubber_service',
                               module_name='parsing',
                               source=site.get("name"),
                               title='Ошибка при парсинге',
                               description=description,
                               error_text=error_text,
                               text_details=text_details,
                               attribute_1=url)


def validation_field_value_per_str(field: str) -> bool:
    return True if field is not None and isinstance(field, str) else False


def validation_field_min_len(field: str, min_len: int) -> bool:
    return True if len(field) > min_len else False


def validation_url(url: str) -> bool:
    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            return True
        else:
            return False

    except Exception as error:
        logger.error(f'URL validation error, text error: {str(error)}')
        traceback.format_exc(limit=None, chain=True)
        return False


def validation_date(date: datetime) -> bool:
    """
    Проверка валидности даты
    :param date: datetime
    :return: None
    """
    return False if date is None and not isinstance(date, datetime.datetime) else True


def validation_title(title: str) -> bool:
    """
    Проверка переданного title на нулевое значение или на строку
    :param title: Заголовок поста
    :return: bool
    """
    return False if title is None and not isinstance(title, str) else True


def validation_link(url: str) -> bool:
    """
    Проверка URL на валидность
    :param grubber_config: GrubberConfig
    :param url: str
    :return: bool
    """
    if url is not None and isinstance(url, str):
        if validation_url(url=url):
            return True

    return False


def parse(download_page_content: str,
          news_site: dict,
          search_time: datetime,
          browser_config: BrowserChromeConfig) -> List[Union[SuccessResponse, MalfunctionResponse]]:
    """
    Функция выполняет парсинг страницы сайта
    """
    parser_response_list = list()
    try:
        logger.debug(f'Parsing site: {news_site.get("name")}, url: {news_site.get("url")}')
        parser = news_site.get('parser_func')
        print(f'parser: {parser}')

        parser_response: List[ParsedData] = parser(site=news_site,
                                                   page_body=download_page_content,
                                                   search_time=search_time,
                                                   browser_config=browser_config)

        if len(parser_response) > 0:
            # Выполняем проверки
            for parsed_data in parser_response:
                # Поверяем ссылку на пост на валидность
                if validation_link(url=parsed_data.more):
                    # проверяем title
                    if validation_title(title=parsed_data.title.text):
                        # проверяем дату
                        if validation_date(date=parsed_data.date):
                            parser_response_list.append(SuccessResponse(status=Status.Ok, content=parser_response))
                            # return SuccessResponse(status=Status.Ok, content=parser_response)
                        else:
                            logger.error(f'A date with an invalid value was received from the parser.'
                                         f'\nresource: {news_site.get("name")}, '
                                         f'\nLink to post: {news_site.get("url")}'
                                         f'\nValue date: {parsed_data.date}')

                            parsed_data.is_valid = False
                            parsed_data.error_content = parsing_error_response(
                                site=news_site,
                                description=f'От парсера получена дата с неверным значением.'
                                            f'\nресурс: {news_site.get("name")}, '
                                            f'\nCсылка на пост: {news_site.get("url")}'
                                            f'\nЗначение date: {parsed_data.date}',
                                error_text=None,
                                text_details=None,
                                url=parsed_data.more)
                    else:
                        logger.error(f'Title received from parser with value None or received a non-string value.'
                                     f'\nresource: {news_site.get("name")}, '
                                     f'\nLink to post: {news_site.get("url")}'
                                     f'\nTitle value: {parsed_data.title}')

                        parsed_data.is_valid = False
                        parsed_data.error_content = parsing_error_response(
                            site=news_site,
                            description=f'От парсера получен title со значением None или получено '
                                        f'значение не являющееся строкой.'
                                        f'\nРесурс: {news_site.get("name")}, '
                                        f'\nCсылка на пост: {news_site.get("url")}'
                                        f'\nЗначение title: {parsed_data.title}',
                            error_text=None,
                            text_details=None,
                            url=parsed_data.more)

                else:
                    logger.error(f'Invalid post link received from parser.'
                                 f'\nResource: {news_site.get("name")}, '
                                 f'\nLink to post: {parsed_data.more}')

                    parsed_data.is_valid = False
                    parsed_data.error_content = parsing_error_response(
                        site=news_site,
                        description=f'От парсера получена невалидная ссылка на пост.'
                                    f'\nРесурс: {news_site.get("name")}, '
                                    f'\nCсылка на пост: {parsed_data.more}',
                        error_text=None,
                        text_details=None,
                        url=None)
        else:
            error_message = (f'No data received from parser function while parsing the site: '
                             f'{news_site.get("name")}, parser function: {news_site.get("parser_func")}')
            logger.warning(error_message)

            # parser_response_list.append(
            #     parsing_error_response(site=site,
            #                            description=f'Ресурс: {site.get("name")}, '
            #                                        f'\nСодержание ошибки: От функции парсера не получено данных',
            #                            error_text="От функции парсера не получено данных",
            #                            text_details=error_message,
            #                            image_parsing_error=grubber_config.image_parsing_error,
            #                            url=site.get("url")))

    except Exception as error:
        logger.error(f'An error occurred while parsing the site: {news_site.get("name")}')
        traceback_text = traceback.format_exc(limit=None, chain=True)
        logger.error(traceback_text)

        parser_response_list.append(parsing_error_response(site=news_site,
                                                           description=f'Ресурс: {news_site.get("name")}, '
                                                                       f'\nСодержание ошибки: {str(error)}'
                                                                       f'\nПодробнее в логе.',
                                                           error_text=str(error),
                                                           text_details=traceback_text,
                                                           url=news_site.get("url")))
    return parser_response_list
