import uuid

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from models.interview_model import InterviewModel, InterviewAnswerModel
from models.pack_model import PackModel
from services.exceptions import PackNotFound, EmptyInterview
from services.interview import InterviewFinishService
from tests.unit.utils import db_inserts


@pytest.mark.asyncio
async def test_get_user_interview_files(
        test_db: AsyncSession, interview_finish_service: InterviewFinishService
):
    pack_id = 1
    interview_id = uuid.uuid4()
    insert_data = {
        PackModel: {
            "id": pack_id,
            "name": "test_pack",
            "intro_file": "intro_file",
            "outro_file": "outro_file",
        },
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
                "answer": "test_answer",
            },
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_1",
                "question_order": 1,
                "answer": "test_answer_1",
            },
        ],
    }
    await db_inserts(test_db, insert_data)

    files = await interview_finish_service.get_user_interview_files(user_id=1)

    assert files == [
        "intro_file",
        "test",
        "test_answer",
        "test_1",
        "test_answer_1",
        "outro_file",
    ]


@pytest.mark.asyncio
async def test_get_user_interview_files_empty_interview(
        test_db: AsyncSession, interview_finish_service: InterviewFinishService
):
    pack_id = 1
    interview_id = uuid.uuid4()
    insert_data = {
        PackModel: {
            "id": pack_id,
            "name": "test_pack",
            "intro_file": "intro_file",
            "outro_file": "outro_file",
        },
        InterviewModel: {
            "id": str(interview_id),
            "user_id": 1,
            "pack_id": pack_id,
            "status": "started",
        },
    }
    await db_inserts(test_db, insert_data)

    with pytest.raises(EmptyInterview):
        await interview_finish_service.get_user_interview_files(user_id=1)


@pytest.mark.asyncio
async def test_get_user_interview_files_no_intro_and_outro(
        test_db: AsyncSession, interview_finish_service: InterviewFinishService
):
    pack_id = 1
    interview_id = uuid.uuid4()
    insert_data = {
        PackModel: {"id": pack_id, "name": "test_pack"},
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
                "answer": "test_answer",
            },
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_1",
                "question_order": 1,
                "answer": "test_answer_1",
            },
        ],
    }
    await db_inserts(test_db, insert_data)

    files = await interview_finish_service.get_user_interview_files(user_id=1)

    assert files == ["test", "test_answer", "test_1", "test_answer_1"]


@pytest.mark.asyncio
async def test_get_interview_finish_file_pack_not_found(
        test_db: AsyncSession, interview_finish_service: InterviewFinishService
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

    interview_finish_service.audio_service.join_files.return_value = "file_bytes"
    with pytest.raises(PackNotFound):
        await interview_finish_service.get_interview_finish_file(user_id=1)


@pytest.mark.asyncio
async def test_get_interview_finish_file(
        test_db: AsyncSession, interview_finish_service: InterviewFinishService
):
    pack_id = 1
    interview_id = uuid.uuid4()
    insert_data = {
        PackModel: {"id": pack_id, "name": "test_pack"},
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
                "answer": "test_answer",
            },
            {
                "id": str(uuid.uuid4()),
                "interview_id": str(interview_id),
                "user_id": 1,
                "question": "test_1",
                "question_order": 1,
                "answer": "test_answer_1",
            },
        ],
    }
    await db_inserts(test_db, insert_data)

    interview_finish_service.audio_service.join_files.return_value = "file_bytes"
    finish_file = await interview_finish_service.get_interview_finish_file(user_id=1)

    assert finish_file == "file_bytes"
