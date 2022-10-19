import uuid
from typing import Optional

from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncEngine

from models.interview_model import InterviewModel, InterviewAnswerModel
from schemas.interview_schema import (
    InterviewUpdate,
    InterviewState,
    InterviewCreate,
    InterviewAnswer,
)


class InterviewRepo:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def create(self, interview: InterviewCreate) -> None:
        async with self.engine.begin() as session:
            query = insert(InterviewModel).values(
                pack_id=interview.pack_id,
                user_id=interview.user_id,
                status=interview.status,
            )

            await session.execute(query)

    async def update(self, user_id: int, interview: InterviewUpdate):
        async with self.engine.begin() as session:
            query = (
                update(InterviewModel)
                .values(
                    status=interview.status,
                )
                .where(
                    InterviewModel.user_id == user_id,
                    InterviewModel.status == InterviewState.started,
                )
            )
            await session.execute(query)

    async def get_user_active_interview(self, user_id: int) -> Optional[dict]:
        async with self.engine.begin() as session:
            query = select(InterviewModel).where(
                InterviewModel.user_id == user_id,
                InterviewModel.status == InterviewState.started,
            )
            result = await session.execute(query)
            return result.fetchone()

    async def add_interview_answer(self, interview_data: InterviewAnswer):
        async with self.engine.begin() as session:
            query = insert(InterviewAnswerModel).values(**interview_data.dict())
            await session.execute(query)

    async def get_interview_answers(self, interview_id: uuid.UUID) -> list[dict]:
        async with self.engine.begin() as session:
            query = select(InterviewAnswerModel).where(
                InterviewAnswerModel.interview_id == interview_id
            )
            return await session.execute(query)
