import logging

from src.config import StorageConfig
from src.utils import create_directory

logger = logging.getLogger(__name__)


def storage_configuration(storage_config: StorageConfig) -> None:
    if storage_config.use_local_directory:
        create_directory(folder_name=storage_config.storage_folder)

    logger.info('Configuration storage is success')