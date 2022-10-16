import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.exceptions import QuestionNotFound
from services.interview import InterviewService, get_interview_service
from models.interview_models import Interview
from schemas.interview_schema import InterviewState


@pytest.mark.asyncio
async def test_get_interview(db: AsyncSession):
    interview: InterviewService = await get_interview_service(1, db)
    await interview.start(1)

    current_interview = await interview._get_interview()
    assert current_interview is not None


@pytest.mark.asyncio
async def test_start_interview(db: AsyncSession):
    interview: InterviewService = await get_interview_service(1, db)
    await interview.start(1)

    db_interview = await db.execute(
        select(
            Interview.id
        ).where(
            Interview.user_id == 1,
            Interview.pack == 1,
            Interview.state == InterviewState.started,
        )
    )

    db_interview = db_interview.first()

    assert db_interview is not None


@pytest.mark.asyncio
async def test_get_next_question(db: AsyncSession):
    interview: InterviewService = await get_interview_service(1, db)
    await interview.start(1)

    next_question = await interview.get_next_question()
    assert next_question == 'pack_1_question_1'


@pytest.mark.asyncio
async def test_save_answer_and_get_next_question(db: AsyncSession):
    interview: InterviewService = await get_interview_service(1, db)
    await interview.start(1)

    first_question = await interview.get_next_question()
    assert first_question == 'pack_1_question_1'

    next_question = await interview.get_next_question('answer_1')
    assert next_question == 'pack_1_question_2'


@pytest.mark.asyncio
async def test_get_interview_finish_files(db: AsyncSession):
    interview: InterviewService = await get_interview_service(1, db)
    await interview.start(1)

    await interview.get_next_question()
    await interview.get_next_question('answer_1')
    try:
        await interview.get_next_question('answer_2')
    except QuestionNotFound:
        ...

    file_ids = await interview._get_file_ids()

    assert file_ids == [
        "intro_pack_1",
        "pack_1_question_1",
        "answer_1",
        "pack_1_question_2",
        "answer_2",
        "outro_pack_1",
    ]
