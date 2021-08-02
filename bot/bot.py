from aiogram.types import Message

from app import dp, bot
from utils.bot_api_helper import get_keyboard_buttons, get_inline_buttons, Button
from services import packs
from services.interview import Interview, QuestionsEnded
from services import audio


interviews_storage = {}


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    chat_id = message.chat.id

    bot.send_message(chat_id, 'Привет! Я возьму у тебя интервью')
    pack_message(chat_id)


@dp.message_handler()
def echo_all(message: Message):
    chat_id = message.chat.id

    if message.text == "завершить":
        finish(chat_id)
    elif message.text == "заново":
        pack_message(chat_id)
    else:
        message.reply("не понял")


@dp.callback_query_handler(regexp='packs_[0-100]')
def pack_choose(call):
    bot.answer_callback_query(
        call.id,
        "отлично, я буду присылать вопрос, а ты мне отвечай голосовым",
        show_alert=False
    )
    chat_id = call.message.chat.id
    pack_id = int(call.data.replace("packs_", ""))

    interview = Interview(chat_id, pack_id)

    keyboard = get_keyboard_buttons([Button(text="завершить")])
    bot.send_voice(chat_id, interview.pack.questions[0], reply_markup=keyboard)
    interviews_storage[chat_id] = interview


@dp.message_handler()
def handle_voice(message: Message) -> None:
    chat_id = message.chat.id
    interview = interviews_storage[chat_id]

    try:
        next_question = interview.save_answer(message.voice.file_id)
    except QuestionsEnded:
        finish(chat_id)
        return

    bot.send_voice(chat_id, next_question)


def pack_message(chat_id: int) -> None:
    buttons = [
        Button(text=pack.name, callback_data=f"packs_{pack.id}")
        for i, pack in packs.get_packs()
    ]

    keyboard = get_inline_buttons(buttons)
    bot.send_message(chat_id, "Выбери пак:", reply_markup=keyboard)


def finish(chat_id: int) -> None:
    keyboard = get_keyboard_buttons([Button(text="завершить")])
    bot.send_message(chat_id, "подожди, я соберу в один файл", reply_markup=keyboard)

    interview = interviews_storage[chat_id]
    file_ids = interview.get_file_ids()

    finish_file = audio.finish_file(file_ids)

    if finish_file is None:
        pack_message(chat_id)
        return

    bot.send_message(chat_id, "готово, лови", reply_markup=keyboard)
    bot.send_audio(chat_id, finish_file)

    # удалим ответы, чтоб не занимать место на сервере
    audio.clear(file_ids)
