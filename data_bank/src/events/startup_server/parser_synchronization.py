import contextlib
from typing import List

from sqlalchemy import select, update, insert

from src.models import SchemeParser
from src.database import get_async_session

from src.parsers import list_parsers


def parsers_to_disable(dp_parsers: List[SchemeParser]) -> List[SchemeParser]:
    disable_parsers: List[SchemeParser] = list()
    for db_parser in dp_parsers:
        is_exist: bool = False

        for parser in list_parsers:
            if db_parser.system_name == parser.get('system_name'):
                is_exist = True

        if is_exist is False:
            disable_parsers.append(db_parser)

    return disable_parsers


def new_parsers(dp_parsers: List[SchemeParser]) -> List[dict]:
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
        dp_parsers: List[SchemeParser] = (await session.execute(select(SchemeParser))).scalars().all()

        # Отключаем в базе данных парсеры, которых нет в списке конфига
        for db_parser in parsers_to_disable(dp_parsers=dp_parsers):
            await session.execute(
                update(SchemeParser)
                .where(SchemeParser.system_name == db_parser.system_name)
                .values(is_parser_scheme_missing=True)
            )
        # Добавляем в базу данных новые парсеры из конфига
        for parser in new_parsers(dp_parsers=dp_parsers):
            await session.execute(
                insert(SchemeParser).values(system_name=parser.get('system_name'),
                                      parser_name=parser.get('parser_name'),
                                      parser_type=parser.get('parser_type'),
                                      is_enable=True,
                                      is_parser_scheme_missing=False)
            )

        await session.commit()
