from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from instruktor.bot.keyboards import main_menu_kb, get_search_kb
from instruktor.botapi import search

search_router = Router()


class Search(StatesGroup):
    search = State()


@search_router.message(F.text == "Поиск")
async def cmd_search(message: Message, state: FSMContext):
    await state.set_state(Search.search)
    await message.answer(text=f"Введите наименование оборудования", reply_markup=main_menu_kb.get_main_menu_back_kb())


@search_router.message(F.text == "Назад", StateFilter(Search.search))
async def cmd_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f"Добро пожаловать", reply_markup=main_menu_kb.get_main_menu_kb())


@search_router.message(F.text, StateFilter(Search.search))
async def cmd_search_name(message: Message, state: FSMContext):
    search_result = await search(tg_id=message.from_user.id, text=message.text)
    await message.answer(text="Выберите результат поиска", reply_markup=get_search_kb(data=search_result))







