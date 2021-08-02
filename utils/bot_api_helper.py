from dataclasses import dataclass

from aiogram import types
from typing import List, Optional


@dataclass
class Button:
    text: str
    callback_data: Optional[str] = None


def remove_keyboard():
    """
    Удаление клавиатуры
    @return:
    """
    return types.ReplyKeyboardRemove()


def get_keyboard_buttons(buttons: List[Button]) -> types.ReplyKeyboardMarkup:
    """
    Формирование кнопок клавиатуры
    @param buttons: список кнопок
    @return: Сформированная клавиатура
    """
    ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(row_width=1)
    for button in buttons:
        KeyboardButton = types.KeyboardButton(button.text)
        ReplyKeyboardMarkup.add(KeyboardButton)

    return ReplyKeyboardMarkup


def get_inline_buttons(buttons: List[Button]) -> types.InlineKeyboardMarkup:
    """
    Формирование кнопок сообщения
    @param buttons: список кнопок
    @return: Сформированная клавиатура
    """
    InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        InlineKeyboardButton = types.InlineKeyboardButton(
            text=button.text,
            callback_data=button.callback_data)
        InlineKeyboardMarkup.add(InlineKeyboardButton)

    return InlineKeyboardMarkup
