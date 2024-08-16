import contextlib

from src.database import get_async_session
from src.parsers import list_parsers


async def sync_db():
    get_async_session_context = contextlib.asynccontextmanager(get_async_session)
    async with get_async_session_context() as session:
        for parser in list_parsers:
            system_name: str = parser.get('system_name')
            parser_name: str = parser.get('parser_name')
            parser_type: str = parser.get('parser_type')
            parser_func: str = parser.get('parser_func')

            dp_parsers = await session.execute(Parser)
            # await session.execute(stmt)
        # await session.commit()


