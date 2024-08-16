import contextlib
import logging
import traceback

from sqlalchemy import delete

from src.auth.manager import get_user_db, get_user_manager
from src.auth.schemes import UserCreate
from src.models import User
from src.config import AdminUserConfig, NewsBotUserConfig, InstructorBotUserConfig, StorageConfig
from src.database import get_async_session

logger = logging.getLogger(__name__)


async def delete_user(user_config: NewsBotUserConfig | InstructorBotUserConfig | AdminUserConfig):
    stmt = (delete(User).where(User.is_superuser == user_config.is_superuser)
            .where(User.is_news_bot == user_config.is_news_bot)
            .where(User.is_instruktor_bot == user_config.is_instruktor_bot))

    get_async_session_context = contextlib.asynccontextmanager(get_async_session)
    async with get_async_session_context() as session:
        await session.execute(stmt)
        await session.commit()


async def create_system_user(email: str,
                             password: str,
                             is_superuser: bool = False,
                             is_news_bot: bool = False,
                             is_instruktor_bot: bool = False) -> None:
    get_async_session_context = contextlib.asynccontextmanager(get_async_session)
    get_user_db_context = contextlib.asynccontextmanager(get_user_db)
    get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                await user_manager.create(UserCreate(email=email,
                                                     password=password,
                                                     is_superuser=is_superuser,
                                                     is_news_bot=is_news_bot,
                                                     is_instruktor_bot=is_instruktor_bot,
                                                     is_active=True,
                                                     is_verified=True))


async def user_configuration(user_config: NewsBotUserConfig | InstructorBotUserConfig | AdminUserConfig) -> None:
    try:
        if user_config.resetting_user:
            await delete_user(user_config=user_config)
            logger.info(f'User: {user_config.username} deleted')
            await create_system_user(email=user_config.username,
                                     password=user_config.password,
                                     is_superuser=user_config.is_superuser,
                                     is_news_bot=user_config.is_news_bot,
                                     is_instruktor_bot=user_config.is_instruktor_bot)
            logger.info(f'User: {user_config.username} created')
        logger.info(f'Configuration user: {user_config.username} is success')
    except Exception as error:
        logger.info(f'{user_config.username}: user configuration error: {error}')
        logger.error(traceback.format_exc(limit=None, chain=True))
