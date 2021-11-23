from typing import Optional

from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from aiogram import Bot

from schemas.bot_schema import InterviewButtons, BotTexts
from db.repositories.pack_repo import get_pack_repo
from services.interview import get_interview_service
from services.exceptions import InterviewNotFound, EmptyInterview, AudioFileGenerationError, QuestionNotFound
from utils.bot_api_helper import get_keyboard_buttons, get_inline_buttons, Button

bot: Optional[Bot] = None


async def send_welcome(message: Message):
    chat_id = message.chat.id

    await bot.send_message(chat_id, BotTexts.WELCOME.value)
    await pack_message(chat_id)


async def text_messages(message: Message):
    chat_id = message.chat.id

    if message.text == InterviewButtons.END:
        await finish(chat_id)
    elif message.text == InterviewButtons.REPEAT:
        await pack_message(chat_id)
    else:
        await message.reply(BotTexts.ERROR.value)


async def pack_choose(call):
    chat_id = call.message.chat.id
    pack_id = int(call.data.replace("packs_", ""))
    keyboard = get_keyboard_buttons([Button(text=InterviewButtons.END.value)])

    await bot.answer_callback_query(call.id)
    await bot.send_message(chat_id, BotTexts.START.value, reply_markup=keyboard)

    interview = await get_interview_service(chat_id)
    await interview.start(pack_id)
    try:
        question = await interview.get_next_question()
        await bot.send_voice(chat_id, question, reply_markup=keyboard)
    except QuestionNotFound:
        await finish(chat_id)


async def handle_voice(message: Message) -> None:
    chat_id = message.chat.id

    interview = await get_interview_service(chat_id)
    try:
        question = await interview.get_next_question(message.voice.file_id)
        await bot.send_voice(chat_id, question)
    except QuestionNotFound:
        await finish(chat_id)
    except InterviewNotFound:
        await finish(chat_id)


async def pack_message(chat_id: int) -> None:
    pack_repo = await get_pack_repo()
    buttons = [
        Button(text=pack.name, callback_data=f"packs_{pack.id}")
        for pack in await pack_repo.get_packs()
    ]

    keyboard = get_inline_buttons(buttons)
    await bot.send_message(chat_id, BotTexts.CHOOSE_PACK.value, reply_markup=keyboard)


async def finish(chat_id: int) -> None:
    interview = await get_interview_service(chat_id)
    keyboard = get_keyboard_buttons([Button(text=InterviewButtons.END.value)])

    await bot.send_message(chat_id, BotTexts.WAIT.value, reply_markup=keyboard)
    try:
        finish_file = await interview.finish()
        await bot.send_message(chat_id, BotTexts.END.value, reply_markup=keyboard)
        await bot.send_audio(chat_id, finish_file)
    except (InterviewNotFound, EmptyInterview, AudioFileGenerationError):
        await pack_message(chat_id)


def register_bot(bot_object: Bot, dp: Dispatcher):
    global bot
    bot = bot_object

    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(text_messages, content_types=ContentType.TEXT)
    dp.register_message_handler(handle_voice, content_types=ContentType.VOICE)
    dp.register_callback_query_handler(pack_choose, regexp='packs_[0-9]')
