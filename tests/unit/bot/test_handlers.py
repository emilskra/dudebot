import uuid
from contextlib import asynccontextmanager
from unittest.mock import patch

from aiogram.types import Message, Chat, CallbackQuery, Voice
from sqlalchemy import select

from core import texts
from handlers.v1.bot import (
    send_welcome,
    pack_message,
    text_messages,
    pack_choose,
    handle_voice,
    finish,
)
from models.interview_model import InterviewModel, InterviewAnswerModel
from models.pack_model import PackModel
from models.question_model import QuestionModel
from tests.unit.utils import db_inserts
from utils.bot_api_helper import get_keyboard_buttons, Button, get_inline_buttons


def assert_pack_send(bot):

    buttons = [
        Button(text="pack1", callback_data=f"packs_1"),
        Button(text="pack2", callback_data=f"packs_2"),
    ]
    keyboard = get_inline_buttons(buttons)
    bot.send_message.assert_any_call(1, texts.CHOOSE_PACK, reply_markup=keyboard)


@asynccontextmanager
async def assert_finish_interview(
    test_db, bot, mocker=None, interview_id=None, interview_answers=None
):
    if mocker:
        join_files = mocker.patch(
            "services.audio.AudioLambda.join_files", return_value="finish_file"
        )
        yield
        join_files.assert_called_with(interview_answers, "1.ogg")
    else:
        yield

    keyboard = get_keyboard_buttons([Button(text=texts.REPEAT)])
    bot.send_message.assert_any_call(1, texts.INTERVIEW_END, reply_markup=keyboard)
    bot.send_audio.assert_any_call(1, "finish_file")

    if interview_id:
        async with test_db.begin() as session:
            interview = await session.execute(
                select(InterviewModel).where(InterviewModel.id == interview_id)
            )
            interview = interview.fetchone()
            assert interview.status == "finish"


async def assert_finish_interview_empty(test_db, bot, interview_id=None):
    assert_pack_send(bot)

    if not interview_id:
        return

    async with test_db.begin() as session:
        interview = await session.execute(
            select(InterviewModel).where(InterviewModel.id == interview_id)
        )
        interview = interview.fetchone()
        assert interview.status == "finish"


async def test_pack_message(test_db, bot):
    packs_data = {PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}]}
    await db_inserts(test_db, packs_data)
    await pack_message(1, bot)

    bot.send_message.assert_called()


async def test_send_welcome(test_db, bot):
    packs_data = {PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}]}
    await db_inserts(test_db, packs_data)

    message = Message(chat=Chat(id=1))
    await send_welcome(message, bot)

    assert_pack_send(bot)


async def test_text_messages_repeat(test_db, bot):
    packs_data = {PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}]}
    await db_inserts(test_db, packs_data)

    message = Message(
        chat=Chat(id=1),
        text=texts.REPEAT,
    )
    await text_messages(message, bot)
    await assert_finish_interview_empty(test_db, bot)


async def test_text_messages_finish(test_db, bot, mocker):
    interview_id = uuid.uuid4()
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": 1,
            "status": "started",
        },
        InterviewAnswerModel: [
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_file",
                "question_order": 0,
                "answer": "test",
            },
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_file_1",
                "question_order": 1,
                "answer": "test_1",
            },
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_file_2",
                "question_order": 2,
                "answer": "test_2",
            },
        ],
    }
    await db_inserts(test_db, data)

    message = Message(
        chat=Chat(id=1),
        text=texts.END,
    )
    interview_answers = [
        "test_file",
        "test",
        "test_file_1",
        "test_1",
        "test_file_2",
        "test_2",
    ]
    async with assert_finish_interview(
        test_db, bot, mocker, interview_id, interview_answers
    ):
        await text_messages(message, bot)


async def test_text_messages_finish_no_interview(test_db, bot):
    packs_data = {PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}]}
    await db_inserts(test_db, packs_data)

    message = Message(
        chat=Chat(id=1),
        text=texts.END,
    )
    await text_messages(message, bot)
    await assert_finish_interview_empty(test_db, bot)


async def test_text_messages_else(test_db, bot):
    packs_data = {PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}]}
    await db_inserts(test_db, packs_data)

    message = Message(
        chat=Chat(id=1),
        text="blabla",
    )

    with patch("aiogram.Bot.get_current", return_value=bot):
        await text_messages(message, bot)

    bot.send_message.assert_called()


async def test_pack_choose(test_db, bot):
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": 1, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": 1, "sort_order": 1},
        ],
    }
    await db_inserts(test_db, data)

    message = Message(
        chat=Chat(id=1),
        text="blabla",
    )
    callback = CallbackQuery(
        message=message,
        data="packs_1",
    )

    await pack_choose(callback, bot)

    keyboard = get_keyboard_buttons([Button(text=texts.END)])
    bot.send_message.assert_called_with(1, texts.START, reply_markup=keyboard)
    bot.send_voice.assert_called_with(1, "test_file")


async def test_handle_first_voice(test_db, bot):
    interview_id = uuid.uuid4()
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": 1, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": 1, "sort_order": 1},
        ],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": 1,
            "status": "started",
        },
    }
    await db_inserts(test_db, data)

    message = Message(chat=Chat(id=1), voice=Voice(file_id="user_voice"))

    await handle_voice(message, bot)

    bot.send_voice.assert_called_with(1, "test_file_2")


async def test_handle_second_voice(test_db, bot):
    interview_id = uuid.uuid4()
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": 1, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": 1, "sort_order": 1},
            {"id": 3, "file_id": "test_file_3", "pack_id": 1, "sort_order": 2},
        ],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": 1,
            "status": "started",
        },
        InterviewAnswerModel: {
            "id": str(uuid.uuid4()),
            "interview_id": str(interview_id),
            "user_id": 1,
            "question": "test_file",
            "question_order": 0,
            "answer": "test",
        },
    }
    await db_inserts(test_db, data)

    message = Message(chat=Chat(id=1), voice=Voice(file_id="user_voice"))

    await handle_voice(message, bot)

    bot.send_voice.assert_called_with(1, "test_file_3")


async def test_handle_the_last_voice(test_db, bot, mocker):
    interview_id = uuid.uuid4()
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": 1, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": 1, "sort_order": 1},
        ],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": 1,
            "status": "started",
        },
        InterviewAnswerModel: {
            "id": str(uuid.uuid4()),
            "interview_id": str(interview_id),
            "user_id": 1,
            "question": "test_file",
            "question_order": 0,
            "answer": "test",
        },
    }
    await db_inserts(test_db, data)

    message = Message(chat=Chat(id=1), voice=Voice(file_id="user_voice"))

    interview_answers = ["test_file", "test", "test_file_2", "user_voice"]
    async with assert_finish_interview(
        test_db, bot, mocker, interview_id, interview_answers
    ):
        await handle_voice(message, bot)


async def test_handle_voice_no_active_interview(test_db, bot):
    interview_id = uuid.uuid4()
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": 1, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": 1, "sort_order": 1},
            {"id": 3, "file_id": "test_file_3", "pack_id": 1, "sort_order": 2},
        ],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": 1,
            "status": "finish",
        },
    }
    await db_inserts(test_db, data)

    message = Message(chat=Chat(id=1), voice=Voice(file_id="user_voice"))

    await handle_voice(message, bot)

    await assert_finish_interview_empty(test_db, bot)


async def test_finish(test_db, bot, mocker):
    interview_id = uuid.uuid4()
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": 1,
            "status": "started",
        },
        InterviewAnswerModel: [
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_file",
                "question_order": 0,
                "answer": "test",
            },
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_file_1",
                "question_order": 1,
                "answer": "test_1",
            },
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_file_2",
                "question_order": 2,
                "answer": "test_2",
            },
        ],
    }
    await db_inserts(test_db, data)

    interview_answers = [
        "test_file",
        "test",
        "test_file_1",
        "test_1",
        "test_file_2",
        "test_2",
    ]
    async with assert_finish_interview(
        test_db, bot, mocker, interview_id, interview_answers
    ):
        await finish(1, bot)


async def test_finish_interview_not_found(test_db, bot):
    interview_id = uuid.uuid4()
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": 1,
            "status": "finish",
        },
    }
    await db_inserts(test_db, data)

    await finish(1, bot)

    await assert_finish_interview_empty(test_db, bot)


async def test_finish_empty_interview(test_db, bot):
    interview_id = uuid.uuid4()
    data = {
        PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": 1,
            "status": "started",
        },
    }
    await db_inserts(test_db, data)

    await finish(1, bot)

    await assert_finish_interview_empty(test_db, bot, interview_id)
