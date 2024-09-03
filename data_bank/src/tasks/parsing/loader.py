import datetime
import logging
import traceback
from typing import Union, Optional

from src.config import BrowserChromeConfig, FormatPostParamsConfig
from src.utils import download_page
from src.utils.classes import SuccessResponse, MalfunctionResponse, Status

logger = logging.getLogger()


def loader_error_response(site: dict, description: Optional[str],
                          error_text: Optional[str], text_details: Optional[str]) -> MalfunctionResponse:
    return MalfunctionResponse(status=Status.Error,
                               date=datetime.datetime.now(),
                               type='error',
                               type_detail='download_error',
                               service_name='grubber_service',
                               module_name='loader',
                               source=site.get("name"),
                               title='Ошибка загрузки',
                               description=description,
                               error_text=error_text,
                               text_details=text_details,
                               attribute_1=site.get("url"))


def download(site: dict,
             format_params: FormatPostParamsConfig,
             browser_config: BrowserChromeConfig) -> Union[SuccessResponse, MalfunctionResponse]:
    try:
        response_page = download_page(url=site.get('url'), config=browser_config)
        if response_page is not None and isinstance(response_page, type) is False:
            if len(response_page) > format_params.len_loaded_content:
                return SuccessResponse(status=Status.Ok, content=response_page)
            else:
                logger.error(f'Error site content: {site.get("name")}, url: "{site.get("url")}", '
                             f'The received content is too small.', )

                return loader_error_response(site=site,
                                             description=f'Полученный от сайта "{site.get("name")}" '
                                                         f'контент менее {format_params.len_loaded_content} символов',
                                             error_text=f'Полученный от сайта "{site.get("name")}" '
                                                         f'контент менее {format_params.len_loaded_content} символов',
                                             text_details=None)
        else:
            logger.error(f'Failed to get content: {site.get("name")}, url: "{site.get("url")}"')

            return loader_error_response(site=site,
                                         description=f'Не удалось получить контент от сайта "{site.get("name")}"',
                                         error_text=f'Не удалось получить контент от сайта "{site.get("name")}"',
                                         text_details=None)

    except Exception as error:
        traceback_text = traceback.format_exc(limit=None, chain=True)
        logger.error(
            f'An unexpected error occurred while downloading, '
            f'site name: {site.get("name")}, url: {site.get("url")}'
        )
        logger.error(traceback_text)

        return loader_error_response(site=site,
                                     description=f'Произошла ошибка при получении данных с сайта, '
                                                 f'ресурс: {site.get("name")}, url: {site.get("url")}'
                                                 f'\nПодробнее в лог файле',
                                     error_text=str(error),
                                     text_details=traceback_text)


