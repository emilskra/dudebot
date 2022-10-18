import uuid

import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.interview_model import InterviewModel, InterviewAnswerModel
from models.question_model import QuestionModel
from schemas.interview_schema import InterviewAnswer
from services.exceptions import InterviewNotFound, QuestionNotFound
from services.interview import InterviewService
from tests.unit.utils import db_inserts


@pytest.mark.asyncio
async def test_start_interview(
    test_db: AsyncSession, interview_service: InterviewService
):
    await interview_service.start_interview(user_id=1, pack_id=2)

    async with test_db.begin() as session:
        created_interview = await session.execute(select(InterviewModel))
        created_interview = created_interview.fetchone()

    assert created_interview.user_id == 1


@pytest.mark.asyncio
async def test_get_user_active_interview(
    test_db: AsyncSession, interview_service: InterviewService
):
    exiting_interview = {
        InterviewModel: {
            "id": str(uuid.uuid4()),
            "user_id": 1,
            "pack_id": 2,
            "status": "started",
        }
    }
    await db_inserts(test_db, exiting_interview)

    interview = await interview_service.get_user_active_interview(user_id=1)

    assert interview.user_id == 1
    assert interview.pack_id == 2


@pytest.mark.asyncio
async def test_get_user_active_interview_not_found(
    test_db: AsyncSession, interview_service: InterviewService
):
    with pytest.raises(InterviewNotFound):
        await interview_service.get_user_active_interview(user_id=1)


@pytest.mark.asyncio
async def test_start_interview_when_there_is_another_one(
    test_db: AsyncSession, interview_service: InterviewService
):
    exiting_interview = {
        InterviewModel: {
            "id": str(uuid.uuid4()),
            "user_id": 1,
            "pack_id": 2,
            "status": "started",
        }
    }
    await db_inserts(test_db, exiting_interview)

    await interview_service.start_interview(user_id=1, pack_id=1)

    async with test_db.begin() as session:
        old_interview = await session.execute(
            select(InterviewModel).where(InterviewModel.pack_id == 2)
        )
        created_interview = await session.execute(
            select(InterviewModel).where(InterviewModel.pack_id == 1)
        )

        old_interview = old_interview.fetchone()
        created_interview = created_interview.fetchone()

    assert old_interview.user_id == 1
    assert old_interview.pack_id == 2
    assert old_interview.status == "finish"

    assert created_interview.user_id == 1
    assert created_interview.pack_id == 1


@pytest.mark.asyncio
async def test_set_interview_finish(
    test_db: AsyncSession, interview_service: InterviewService
):
    exiting_interview = {
        InterviewModel: {
            "id": str(uuid.uuid4()),
            "user_id": 1,
            "pack_id": 2,
            "status": "started",
        }
    }
    await db_inserts(test_db, exiting_interview)

    await interview_service.set_interview_finish(user_id=1)

    async with test_db.begin() as session:
        created_interview = await session.execute(
            select(InterviewModel).where(InterviewModel.pack_id == 2)
        )
        created_interview = created_interview.fetchone()

    assert created_interview.user_id == 1
    assert created_interview.pack_id == 2
    assert created_interview.status == "finish"


@pytest.mark.asyncio
async def test_get_next_interview_question(
    test_db: AsyncSession, interview_service: InterviewService
):
    pack_id = 1
    insert_data = {
        InterviewModel: {
            "id": str(uuid.uuid4()),
            "user_id": 1,
            "pack_id": pack_id,
            "status": "started",
        },
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": pack_id, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": pack_id, "sort_order": 1},
        ],
    }
    await db_inserts(test_db, insert_data)
    question = await interview_service.get_next_question(user_id=1)
    assert question.file_id == "test_file"


@pytest.mark.asyncio
async def test_get_next_interview_question_interview_not_found(
    test_db: AsyncSession, interview_service: InterviewService
):
    pack_id = 1
    insert_data = {
        InterviewModel: {
            "id": str(uuid.uuid4()),
            "user_id": 1,
            "pack_id": pack_id,
            "status": "finish",
        },
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": pack_id, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": pack_id, "sort_order": 1},
        ],
    }
    await db_inserts(test_db, insert_data)
    with pytest.raises(InterviewNotFound):
        await interview_service.get_next_question(user_id=1)


@pytest.mark.asyncio
async def test_get_next_interview_question_not_found(
    test_db: AsyncSession, interview_service: InterviewService
):
    pack_id = 1
    insert_data = {
        InterviewModel: {
            "id": str(uuid.uuid4()),
            "user_id": 1,
            "pack_id": pack_id,
            "status": "started",
        },
    }
    await db_inserts(test_db, insert_data)
    with pytest.raises(QuestionNotFound):
        await interview_service.get_next_question(user_id=1)


@pytest.mark.asyncio
async def test_save_interview_answer(
    test_db: AsyncSession, interview_service: InterviewService
):
    interview_id = uuid.uuid4()
    pack_id = 1
    insert_data = {
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": pack_id, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": pack_id, "sort_order": 1},
        ],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": pack_id,
            "status": "started",
        },
    }
    await db_inserts(test_db, insert_data)

    await interview_service.save_answer(user_id=1, answer_file="test")

    async with test_db.begin() as session:
        result = await session.execute(
            select(
                InterviewAnswerModel.interview_id, InterviewAnswerModel.question_order
            )
        )
        result = result.fetchall()

    assert result == [(interview_id, 0)]


@pytest.mark.asyncio
async def test_save_interview_next_answer(
    test_db: AsyncSession, interview_service: InterviewService
):
    pack_id = 1
    interview_id = uuid.uuid4()
    insert_data = {
        QuestionModel: [
            {"id": 1, "file_id": "test_file", "pack_id": pack_id, "sort_order": 0},
            {"id": 2, "file_id": "test_file_2", "pack_id": pack_id, "sort_order": 1},
        ],
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": pack_id,
            "status": "started",
        },
        InterviewAnswerModel: {
            "id": str(uuid.uuid4()),
            "interview_id": str(interview_id),
            "user_id": 1,
            "question": "test",
            "question_order": 0,
            "answer": "test",
        },
    }
    await db_inserts(test_db, insert_data)

    await interview_service.save_answer(user_id=1, answer_file="test2")

    async with test_db.begin() as session:
        result = await session.execute(
            select(
                InterviewAnswerModel.interview_id, InterviewAnswerModel.answer
            ).where(InterviewAnswerModel.user_id == 1)
        )
        result = result.fetchall()

    assert result == [
        (interview_id, "test"),
        (interview_id, "test2"),
    ]


@pytest.mark.asyncio
async def test_save_interview_next_answer_interview_not_found(
    test_db: AsyncSession, interview_service: InterviewService
):
    pack_id = 1
    interview_id = uuid.uuid4()
    insert_data = {
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": pack_id,
            "status": "finish",
        },
    }
    await db_inserts(test_db, insert_data)

    with pytest.raises(InterviewNotFound):
        await interview_service.save_answer(user_id=1, answer_file="test2")


@pytest.mark.asyncio
async def test_get_user_interview_answers(
    test_db: AsyncSession, interview_service: InterviewService
):
    pack_id = 1
    interview_id = uuid.uuid4()
    insert_data = {
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": pack_id,
            "status": "started",
        },
        InterviewAnswerModel: [
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test",
                "question_order": 0,
                "answer": "test",
            },
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_1",
                "question_order": 1,
                "answer": "test_1",
            },
        ],
    }
    await db_inserts(test_db, insert_data)

    answers = await interview_service.get_user_interview_answers(user_id=1)
    assert answers == [
        InterviewAnswer(
            user_id=1,
            interview_id=interview_id,
            answer="test",
            question="test",
            question_order=0,
        ),
        InterviewAnswer(
            user_id=1,
            interview_id=interview_id,
            answer="test_1",
            question="test_1",
            question_order=1,
        ),
    ]
