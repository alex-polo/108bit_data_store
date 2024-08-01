from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from instruktor.bot.keyboards import main_menu_kb

main_menu_router = Router()


@main_menu_router.message(F.text == "Главное меню")
@main_menu_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f"Добро пожаловать", reply_markup=main_menu_kb.get_main_menu_kb())
