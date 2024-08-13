from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_manufacturers_kb(data: list) -> ReplyKeyboardMarkup:
    mf_kb = ReplyKeyboardBuilder()
    for obj in data:
        mf_kb.button(text=f"{obj}")
    mf_kb.adjust(2)
    mf_kb.row(KeyboardButton(text="Назад"))
    return mf_kb.as_markup(resize_keyboard=True)
