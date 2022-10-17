from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from core import texts
from services.pack import PackService
from services.base import get_service
from services.interview import InterviewService, InterviewFinishService
from services.exceptions import InterviewNotFound, EmptyInterview, QuestionNotFound
from utils.bot_api_helper import (
    get_keyboard_buttons,
    get_inline_buttons,
    remove_keyboard,
    Button,
)


async def send_welcome(message: Message, bot: Bot):
    chat_id = message.chat.id

    await bot.send_message(chat_id, texts.WELCOME)
    await pack_message(bot=bot, chat_id=chat_id)


async def text_messages(message: Message, bot: Bot):
    chat_id = message.chat.id
    if message.text == texts.END:
        await finish(bot=bot, chat_id=chat_id)
    elif message.text == texts.REPEAT:
        await pack_message(bot=bot, chat_id=chat_id)
    else:
        await message.reply(texts.ERROR)


async def pack_choose(call: CallbackQuery, bot: Bot):
    interview_service = get_service(InterviewService)

    chat_id = call.message.chat.id
    pack_id = int(call.data.replace("packs_", ""))
    keyboard = get_keyboard_buttons([Button(text=texts.END)])

    await bot.answer_callback_query(call.id)
    await bot.send_message(chat_id, texts.START, reply_markup=keyboard)

    await interview_service.start_interview(pack_id, chat_id)
    try:
        question = await interview_service.get_next_question(chat_id)
        await bot.send_voice(chat_id, question, reply_markup=keyboard)
    except QuestionNotFound:
        await finish(bot=bot, chat_id=chat_id)


async def handle_voice(message: Message, bot: Bot) -> None:
    interview_service = get_service(InterviewService)

    chat_id = message.chat.id

    try:
        await interview_service.save_answer(chat_id, message.voice.file_id)
        question = await interview_service.get_next_question(chat_id)
        await bot.send_voice(chat_id, question)
    except QuestionNotFound:
        await finish(bot=bot, chat_id=chat_id)
    except InterviewNotFound:
        await bot.send_message(chat_id, texts.INTERVIEW_NOT_STARTED)
        await pack_message(bot=bot, chat_id=chat_id)


async def pack_message(chat_id: int, bot: Bot) -> None:
    pack_service = get_service(PackService)

    buttons = [
        Button(text=pack.name, callback_data=f"packs_{pack.id}")
        for pack in await pack_service.get_all()
    ]

    keyboard = get_inline_buttons(buttons)
    await bot.send_message(chat_id, texts.CHOOSE_PACK, reply_markup=keyboard)


async def finish(chat_id: int, bot: Bot) -> None:
    interview_service = get_service(InterviewService)
    interview_finish_service = get_service(InterviewFinishService)

    keyboard = get_keyboard_buttons([Button(text=texts.REPEAT)])
    remove = remove_keyboard()

    await bot.send_message(chat_id, texts.WAIT, reply_markup=remove)
    try:
        finish_file = await interview_finish_service.get_interview_finish_file(chat_id)

        await bot.send_message(chat_id, texts.INTERVIEW_END, reply_markup=keyboard)
        await bot.send_audio(chat_id, finish_file)

        await interview_service.set_interview_finish(chat_id)
    except (InterviewNotFound, EmptyInterview):
        await pack_message(bot=bot, chat_id=chat_id)
