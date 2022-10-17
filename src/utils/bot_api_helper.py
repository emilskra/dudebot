from dataclasses import dataclass

from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)
from typing import List, Optional


@dataclass
class Button:
    text: str
    callback_data: Optional[str] = None


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def get_keyboard_buttons(buttons: List[Button]) -> ReplyKeyboardMarkup:
    reply_keyboard = ReplyKeyboardMarkup(row_width=1)
    for button in buttons:
        keyboard_button = KeyboardButton(button.text)
        reply_keyboard.add(keyboard_button)

    return reply_keyboard


def get_inline_buttons(buttons: List[Button]) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        inline_button = InlineKeyboardButton(
            text=button.text, callback_data=button.callback_data
        )
        inline_keyboard.add(inline_button)

    return inline_keyboard
