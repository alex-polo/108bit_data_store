import asyncio
from typing import Optional

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from instruktor.bot.handlers import main_menu_router, search_router, parser_router
from instruktor.config import BotConfig

storage = MemoryStorage()

BOT: Optional[Bot] = None
DP: Optional[Dispatcher] = None


def create_dispatcher() -> Dispatcher():
    disp = Dispatcher()
    disp.include_routers(main_menu_router, search_router, parser_router)
    return disp


async def main(bot_config: BotConfig) -> None:
    global BOT, DP
    BOT = Bot(bot_config.token)
    DP = create_dispatcher()
    await DP.start_polling(BOT)


def run(bot_config: BotConfig) -> None:
    asyncio.run(main(bot_config=bot_config))
