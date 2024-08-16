import logging

from .configuration_storage import storage_configuration
from .configuration_users import user_configuration
from src.config import (
    AdminUserConfig,
    NewsBotUserConfig,
    InstructorBotUserConfig,
    StorageConfig)

logger = logging.getLogger(__name__)


async def on_startup(admin_user_config: AdminUserConfig,
                     news_bot_user_config: NewsBotUserConfig,
                     instructor_bot_user_config: InstructorBotUserConfig,
                     storage_config: StorageConfig) -> None:
    logger.info('Configuration storage')
    storage_configuration(storage_config=storage_config)

    logger.info('Configuration system users')
    await user_configuration(user_config=admin_user_config)
    await user_configuration(user_config=news_bot_user_config)
    await user_configuration(user_config=instructor_bot_user_config)
