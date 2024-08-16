import logging
import os
import platform

from environs import Env
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .classes import (
    DatabaseConfig,
    StorageConfig,
    AdminUserConfig,
    NewsBotUserConfig,
    InstructorBotUserConfig,
    AuthConfig,
    BrowserChromeConfig,
    ServerConfig, CeleryConfig)

from .settings import (win_webdriver_path,
                       linux_webdriver_path,
                       webdriver_port,
                       webdriver_timeout,
                       chrome_page_load_strategy,
                       chrome_options, celery_logging_config)

logger = logging.getLogger(__name__)


def get_database_config() -> DatabaseConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    return DatabaseConfig(
        DB_USER=env.str('DB_USER'),
        DB_PASS=env.str('DB_PASS'),
        DB_HOST=env.str('DB_HOST'),
        DB_PORT=env.str('DB_PORT'),
        DB_NAME=env.str('DB_NAME'),
    )


def get_storage_config() -> StorageConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    return StorageConfig(
        use_cloud=True if env.str('USE_CLOUD') == 'YES' else False,
        use_local_directory=True if env.str('USE_LOCAL_DIRECTORY') == 'YES' else False,
        url_yandex_disk=env.str('YANDEX_DISK_URL'),
        storage_folder=env.str('LOCAL_DIRECTORY')
    )


def get_admin_user_config() -> AdminUserConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))
    return AdminUserConfig(
        username=env.str('ADMIN_USER_LOGIN'),
        password=env.str('ADMIN_USER_PASSWORD'),
        resetting_user=True if env.str('RESETTING_ADMIN_USER') == 'YES' else False,
        is_superuser=True,
        is_news_bot=False,
        is_instruktor_bot=False
    )


def get_news_bot_user_config() -> NewsBotUserConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))
    return NewsBotUserConfig(
        username=env.str('NEWS_BOT_USER_LOGIN'),
        password=env.str('NEWS_BOT_USER_PASSWORD'),
        resetting_user=True if env.str('RESETTING_NEWS_BOT_USER') == 'YES' else False,
        is_superuser=False,
        is_news_bot=True,
        is_instruktor_bot=False
    )


def get_instructor_bot_user_config() -> InstructorBotUserConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))
    return InstructorBotUserConfig(
        username=env.str('INSTRUKTOR_BOT_USER_LOGIN'),
        password=env.str('INSTRUKTOR_BOT_USER_PASSWORD'),
        resetting_user=True if env.str('RESETTING_INSTRUKTOR_BOT_USER') == 'YES' else False,
        is_superuser=False,
        is_news_bot=False,
        is_instruktor_bot=True
    )


def get_auth_config() -> AuthConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    return AuthConfig(
        auth_secret_key=env.str('AUTH_SECRET_KEY')
    )


def get_browser_chrome_config() -> BrowserChromeConfig:
    # Опции браузера
    options: Options = webdriver.ChromeOptions()
    for option in chrome_options:
        options.add_argument(option)

    # Путь до драйвера в зависимости от ОС
    path: str = win_webdriver_path if platform.system() == 'Windows' else linux_webdriver_path

    return BrowserChromeConfig(
        options=options,
        load_strategy=chrome_page_load_strategy,
        driver_path=os.path.join(os.getcwd(), path),
        port=webdriver_port,
        timeout=webdriver_timeout,
    )


def get_server_config() -> ServerConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    try:
        with open(os.path.join(os.getcwd(), 'version.txt'), 'r') as file:
            version = file.read()
    except Exception as error:
        logger.error(error)
        version = 'version is bad'

    return ServerConfig(
        version=version,
        https=True if env.str('HTTPS') == 'YES' else False
    )


def get_celery_config() -> CeleryConfig:
    env = Env()
    env.read_env(os.path.join(os.getcwd(), '.env'))

    return CeleryConfig(
        LOGGING_CONFIG=os.path.join(os.getcwd(), celery_logging_config),
        BROKER=env.str('CELERY_BROKER'),
        BACKEND=env.str('CELERY_BACKEND'),
    )
