import datetime
import logging
import os
import traceback
from typing import Union, Optional

from src.config import FormatPostParamsConfig
from src.tasks.parsing.news_parsing import validation_field_value_per_str, validation_url
from src.utils.classes import (
    ParsedData,
    SuccessResponse,
    MalfunctionResponse,
    Status,
    ParserField,
    FormatField,
    PostData
)

logger = logging.getLogger()


def post_editor_malfunction_error_response(site: dict, description: Optional[str], error_text: Optional[str],
                                           text_details: Optional[str]) -> MalfunctionResponse:
    return MalfunctionResponse(status=Status.Error,
                               date=datetime.datetime.now(),
                               type='error',
                               type_detail='post_editor_error',
                               service_name='grubber_service',
                               module_name='post_editor',
                               source=site.get("name"),
                               title='Ошибка при обработке данных полученных от парсера',
                               description=description,
                               error_text=error_text,
                               text_details=text_details,
                               attribute_1=site.get("url"))


def post_editor_malfunction_warning_response(site: dict,
                                             warning_text: Optional[str]) -> MalfunctionResponse:
    return MalfunctionResponse(status=Status.Warning,
                               date=datetime.datetime.now(),
                               type='warning',
                               type_detail='post_editor_warning',
                               service_name='grubber_service',
                               module_name='post_editor',
                               source=site.get("name"),
                               title='Получены некорректные данные от парсера',
                               description=warning_text,
                               error_text=None,
                               text_details=None,
                               attribute_1=site.get("url"))


def inserting_special_characters_into_field(field: str) -> str:
    field = field.replace('$space$', ' ')
    field = field.replace('$new_line$', '\n')

    return field


# def main_image(site: dict) -> Optional[str]:
#     if site.get('image_path') is not None:
#         if os.path.exists(site.get('image_path')):
#             return site.get('image_path')
#         else:
#             return None


def remove_spaces_and_line_breaks(text: str) -> str:
    """
    Функция удаляет лишнии пробелы в конце и начале строки, а также все переносы каретки
    :param text: Входная строка
    :return: str
    """
    text = text.strip()
    text = text.replace('\r', '')
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    return text


def shops_by_words(text: str, max_len: int) -> str:
    """
    Функция выполняет обрезку строки если ее длина больше параметра max_len.
    Обрезка выполняется по последнему целому слову
    :param text: Входная строка
    :param max_len: Максимальная длина строки
    :return:str
    """
    if len(text) > max_len:
        key_words = text[: max_len].split(' ')
        words = text.split(' ')
        return f'{" ".join([word for word in key_words if word in words])} ...'
    elif text[-1] == ':':
        return f'{text} ...'
    else:
        return text


def format_text_field(field: str, field_value: Optional[ParserField],
                      min_len: int, max_len: int,
                      site: dict) -> FormatField:
    """
    Форматируем переданное поле
    :param field:
    :param field_value:
    :param min_len:
    :param max_len:
    :param site:
    :return:
    """
    warning_message: Optional[str] = None

    if validation_field_value_per_str(field=field_value.text):
        if field_value.is_format:
            status = Status.Ok
            value = field_value.text
        else:
            if field == 'details':
                details = finishing_format_details(details=field_value.text)
            else:
                details = field_value.text
            value = remove_spaces_and_line_breaks(details)
            if len(value) > min_len:
                status = Status.Ok
                value = inserting_special_characters_into_field(shops_by_words(value, max_len))

            else:
                status = Status.Warning
                warning_message = f'Поле "{field}" имеет длину меньше или равную минимальной,' \
                                  f'\nДлина поля: {len(value)}' \
                                  f'\nРекомендуемая минимальная длина: {min_len}'
    else:
        status = Status.Warning
        value = ''
        warning_message = f'Значение поля "{field}" не является строкой, значение: {field_value.text}'

    return FormatField(
        status=status,
        field_name=field,
        field_value=value,
        warning_message=None if warning_message is None else post_editor_malfunction_warning_response(
            site=site,
            warning_text=warning_message)
    )


def image_post_formation(url: str) -> Optional[str]:
    # Проверяем значение переменной
    if url is not None and isinstance(url, str) and len(url) > 0:
        if validation_url(url=url):
            return url
    else:
        return None


def validation_len_title(title, min_len: int, max_len: int) -> bool:
    return min_len < len(title) < max_len


def finishing_format_details(details: str) -> str:
    return '$new_line$$new_line$'.join(
        [' '.join(details_line.strip().split()) for details_line in details.split('\n')
         if len(details_line.strip()) > 0]
    )


def post_formation(parsed_data: ParsedData,
                   site: dict,
                   format_params: FormatPostParamsConfig) -> Union[SuccessResponse, MalfunctionResponse]:
    """
    Функция формирует пост
    """
    logger.debug(f'Formatting of the post, input data: {parsed_data}')
    try:
        malfunctions = list()

        format_title = format_text_field(field='title',
                                         field_value=parsed_data.title,
                                         min_len=format_params.formatting_min_len_title,
                                         max_len=format_params.formatting_len_title,
                                         site=site)

        format_details = format_text_field(field='details',
                                           field_value=parsed_data.details,
                                           min_len=format_params.formatting_min_len_details,
                                           max_len=format_params.formatting_len_details,
                                           site=site)

        if format_title.warning_message is not None:
            format_title.warning_message.description = f'{format_title.warning_message.description}' \
                                                       f'\nДанные о новости:' \
                                                       f'\nДата: {parsed_data.date}' \
                                                       f'\nЗаголовок: {parsed_data.title}'

            format_title.warning_message.attribute_1 = parsed_data.more

            malfunctions.append(format_title.warning_message)

        if format_details.warning_message is not None:
            format_details.warning_message.description = f'{format_details.warning_message.description}' \
                                                         f'\n\nДанные о новости:' \
                                                         f'\nДата: {parsed_data.date.strftime("%d-%m-%Y")}' \
                                                         f'\nЗаголовок: {parsed_data.title}'
            format_details.warning_message.attribute_1 = parsed_data.more

            malfunctions.append(format_details.warning_message)

        image = image_post_formation(url=parsed_data.image_url)

        return SuccessResponse(
            status=Status.Ok,
            content=PostData(
                status=Status.Ok,
                date=parsed_data.date,
                title=format_title.field_value,
                details=format_details.field_value,
                more=parsed_data.more,
                image_url=image,
                main_tag=None,
                fields_tags=None,
                author=None,
                malfunctions=malfunctions
            )
        )
    except Exception as error:
        text_traceback = traceback.format_exc(limit=None, chain=True)
        logger.error(error)
        logger.error(text_traceback)
        return post_editor_malfunction_error_response(site=site,
                                                      description=f'Произошла ошибка при формировании поста.'
                                                                  f'\nТекст ошибки: \n{str(error)}.'
                                                                  f'\nПодробнее в логе.',
                                                      error_text=str(error),
                                                      text_details=text_traceback)
