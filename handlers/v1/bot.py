from aiogram.types import Message, ContentType

from app import dp, bot
from schemas.buttons_schema import InterviewButtons
from services.audio import get_audio
from services.exceptions import InterviewNotFound
from utils.bot_api_helper import get_keyboard_buttons, get_inline_buttons, Button
from services import packs
from services.interview import QuestionsEnded, get_interview_service


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    chat_id = message.chat.id

    await bot.send_message(chat_id, 'Привет! Я возьму у тебя интервью')
    await pack_message(chat_id)


@dp.message_handler(content_types=ContentType.TEXT)
async def echo_all(message: Message):
    chat_id = message.chat.id

    if message.text == InterviewButtons.end:
        await finish(chat_id)
    elif message.text == InterviewButtons.repeat:
        await pack_message(chat_id)
    else:
        await message.reply("не понял")


@dp.callback_query_handler(regexp='packs_[0-9]')
async def pack_choose(call):
    bot.answer_callback_query(
        call.id,
        "отлично, я буду присылать вопрос, а ты мне отвечай голосовым сообщением",
        show_alert=False
    )
    chat_id = call.message.chat.id
    pack_id = int(call.data.replace("packs_", ""))

    interview = get_interview_service(chat_id)
    await interview.start(pack_id)

    question = await interview.get_next_question()

    keyboard = get_keyboard_buttons([Button(text="завершить")])
    await bot.send_voice(chat_id, question, reply_markup=keyboard)


@dp.message_handler(content_types=ContentType.VOICE)
async def handle_voice(message: Message) -> None:
    chat_id = message.chat.id

    interview = get_interview_service(chat_id)
    try:
        await interview.save_answer(message.voice.file_id)
        next_question = await interview.get_next_question()
    except QuestionsEnded:
        await finish(chat_id)
    except InterviewNotFound:
        await finish(chat_id)
    else:
        await bot.send_voice(chat_id, next_question)


async def pack_message(chat_id: int) -> None:
    buttons = [
        Button(text=pack.name, callback_data=f"packs_{pack.id}")
        for i, pack in packs.get_packs()
    ]

    keyboard = get_inline_buttons(buttons)
    bot.send_message(chat_id, "Выбери пак:", reply_markup=keyboard)


async def finish(chat_id: int) -> None:
    interview = get_interview_service(chat_id)
    keyboard = get_keyboard_buttons([Button(text="завершить")])
    bot.send_message(chat_id, "подожди, я соберу в один файл", reply_markup=keyboard)

    file_ids = await interview.get_file_ids()

    audio = get_audio()
    finish_file = await audio.get_finish_file(file_ids)

    if finish_file is None:
        await pack_message(chat_id)
        return

    await bot.send_message(chat_id, "готово, лови", reply_markup=keyboard)
    await bot.send_audio(chat_id, finish_file)

    await audio.clear(file_ids)
