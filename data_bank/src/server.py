import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from src.auth.routers import auth_router
from src.events import on_startup
from src.config import (
    AdminUserConfig,
    NewsBotUserConfig,
    InstructorBotUserConfig,
    StorageConfig,
    get_news_bot_user_config,
    get_instructor_bot_user_config,
    get_storage_config,
    get_admin_user_config, BrowserChromeConfig, get_browser_chrome_config, get_server_config, ServerConfig)

logger = logging.getLogger(__name__)

server_config: ServerConfig = get_server_config()


async def start_server() -> None:
    """
    Функция выполняется при старте сервера
    :return: None
    """
    logger.info('Reading configuration server')
    admin_user_config: AdminUserConfig = get_admin_user_config()
    news_bot_user_config: NewsBotUserConfig = get_news_bot_user_config()
    instructor_bot_user_config: InstructorBotUserConfig = get_instructor_bot_user_config()
    storage_config: StorageConfig = get_storage_config()
    browser_chrome_config: BrowserChromeConfig = get_browser_chrome_config()

    await on_startup(admin_user_config=admin_user_config,
                     news_bot_user_config=news_bot_user_config,
                     instructor_bot_user_config=instructor_bot_user_config,
                     storage_config=storage_config)


def shutdown_server() -> None:
    """ Функция выполняется при остановке сервиса """
    pass


origins = [
    "https://127.0.0.1:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://localhost:5173"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Start startup events')
    await start_server()
    yield
    logger.info('lifespan end')


app = FastAPI(
    title='DataBank',
    version=server_config.version,
    lifespan=lifespan
)

if server_config.https:
    app.add_middleware(HTTPSRedirectMiddleware, )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(auth_router)
