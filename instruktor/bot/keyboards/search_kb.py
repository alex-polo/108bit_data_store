from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_search_kb(data: str) -> ReplyKeyboardMarkup:
    search_list_kb = ReplyKeyboardBuilder()
    for sr in data:
        search_list_kb.button(text=f"{sr}")
    search_list_kb.adjust(2)
    search_list_kb.row(KeyboardButton(text="Назад"))
    return search_list_kb.as_markup(resize_keyboard=True)
