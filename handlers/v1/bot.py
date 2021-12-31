from typing import Optional

from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.bot_schema import InterviewButtons, BotTexts
from db.repositories.pack_repo import get_pack_repo
from services.interview import get_interview_service
from services.exceptions import InterviewNotFound, EmptyInterview, AudioFileGenerationError, QuestionNotFound
from services.storages.telegram_storage import set_bot
from utils.bot_api_helper import get_keyboard_buttons, get_inline_buttons, remove_keyboard, Button

bot: Optional[Bot] = None


async def send_welcome(message: Message, db: AsyncSession):
    chat_id = message.chat.id

    await bot.send_message(chat_id, BotTexts.WELCOME.value)
    await pack_message(chat_id, db)


async def text_messages(message: Message, db: AsyncSession):
    chat_id = message.chat.id

    if message.text == InterviewButtons.END:
        await finish(chat_id, db)
    elif message.text == InterviewButtons.REPEAT:
        await pack_message(chat_id, db)
    else:
        await message.reply(BotTexts.ERROR.value)


async def pack_choose(call, db: AsyncSession):
    chat_id = call.message.chat.id
    pack_id = int(call.data.replace("packs_", ""))
    keyboard = get_keyboard_buttons([Button(text=InterviewButtons.END.value)])

    await bot.answer_callback_query(call.id)
    await bot.send_message(chat_id, BotTexts.START.value, reply_markup=keyboard)

    interview = await get_interview_service(chat_id, db)
    await interview.start(pack_id)
    try:
        question = await interview.get_next_question()
        await bot.send_voice(chat_id, question, reply_markup=keyboard)
    except QuestionNotFound:
        await finish(chat_id, db)


async def handle_voice(message: Message, db: AsyncSession) -> None:
    chat_id = message.chat.id

    interview = await get_interview_service(chat_id, db)
    try:
        question = await interview.get_next_question(message.voice.file_id)
        await bot.send_voice(chat_id, question)
    except QuestionNotFound:
        await finish(chat_id, db)
    except InterviewNotFound:
        await pack_message(chat_id, db)


async def pack_message(chat_id: int, db: AsyncSession) -> None:
    pack_repo = await get_pack_repo(db)
    buttons = [
        Button(text=pack.name, callback_data=f"packs_{pack.id}")
        for pack in await pack_repo.get_packs()
    ]

    keyboard = get_inline_buttons(buttons)
    await bot.send_message(chat_id, BotTexts.CHOOSE_PACK.value, reply_markup=keyboard)


async def finish(chat_id: int, db: AsyncSession) -> None:
    interview = await get_interview_service(chat_id, db)
    keyboard = get_keyboard_buttons([Button(text=InterviewButtons.REPEAT.value)])
    remove = remove_keyboard()

    await bot.send_message(chat_id, BotTexts.WAIT.value, reply_markup=remove)
    try:
        async with interview.finish() as finish_file:
            await bot.send_message(chat_id, BotTexts.END.value, reply_markup=keyboard)
            await bot.send_audio(chat_id, finish_file)
    except (InterviewNotFound, EmptyInterview, AudioFileGenerationError):
        await pack_message(chat_id, db)


def register_bot(bot_object: Bot, dp: Dispatcher):
    global bot
    bot = bot_object

    set_bot(bot_object)

    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(text_messages, content_types=ContentType.TEXT)
    dp.register_message_handler(handle_voice, content_types=ContentType.VOICE)
    dp.register_callback_query_handler(pack_choose, regexp='packs_[0-9]')
