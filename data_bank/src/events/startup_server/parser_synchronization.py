import contextlib
from typing import List

from sqlalchemy import select, update, insert

from src.models import Parser
from src.database import get_async_session

from src.parsers import list_parsers


def parsers_to_disable(dp_parsers: List[Parser]) -> List[Parser]:
    disable_parsers: List[Parser] = list()
    for db_parser in dp_parsers:
        is_exist: bool = False

        for parser in list_parsers:
            if db_parser.system_name == parser.get('system_name'):
                is_exist = True

        if is_exist is False:
            disable_parsers.append(db_parser)

    return disable_parsers


def new_parsers(dp_parsers: List[Parser]) -> List[dict]:
    new_parsers_list: List[dict] = list()
    for parser in list_parsers:
        is_exist: bool = False
        for db_parser in dp_parsers:
            if db_parser.system_name == parser.get('system_name'):
                is_exist = True

        if is_exist is False:
            new_parsers_list.append(parser)

    return new_parsers_list


async def synchronizing_list_parsers_with_database() -> None:
    get_async_session_context = contextlib.asynccontextmanager(get_async_session)
    async with get_async_session_context() as session:
        dp_parsers: List[Parser] = (await session.execute(select(Parser))).scalars().all()

        # Отключаем в базе данных парсеры, которых нет в списке конфига
        # Парсеры у которых совпадает системное имя не трогаем
        # Добавляем в базу данных новые парсеры из конфига
        for db_parser in parsers_to_disable(dp_parsers=dp_parsers):
            await session.execute(
                update(Parser).where(Parser.system_name == db_parser.system_name).values(is_enable=False)
            )

        for parser in new_parsers(dp_parsers=dp_parsers):
            await session.execute(
                insert(Parser).values(system_name=parser.get('system_name'),
                                      parser_name=parser.get('parser_name'),
                                      parser_type=parser.get('parser_type'),
                                      is_enable=True)
            )

        await session.commit()
