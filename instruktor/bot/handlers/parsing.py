from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from instruktor.bot.keyboards import get_manufacturers_kb, main_menu_kb
from instruktor.botapi import manufacturers

parser_router = Router()


class Parsing(StatesGroup):
    initiation = State()


@parser_router.message(F.text == "Выбор производителя")
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Parsing.initiation)
    mf_list = manufacturers(message.from_user.id)
    await message.answer(text=f"Выберите производителя оборудования", reply_markup=get_manufacturers_kb(mf_list))


@parser_router.message(F.text == "Назад", StateFilter(Parsing.initiation))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f"Добро пожаловать", reply_markup=main_menu_kb.get_main_menu_kb())
