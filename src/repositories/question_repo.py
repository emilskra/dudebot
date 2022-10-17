import uuid
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from models.interview_model import InterviewAnswerModel
from models.question_model import QuestionModel
from schemas.question_schema import Question


class QuestionRepo:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def get_pack_question(self, pack_id: int, sort_order: int) -> QuestionModel:
        async with self.engine.begin() as session:
            query = select(QuestionModel).where(
                QuestionModel.pack_id == pack_id,
                QuestionModel.sort_order == sort_order,
            )
            result = await session.execute(query)
            return result.fetchone()

    async def get_interview_last_question_order(
        self, interview_id: uuid.UUID
    ) -> Optional[int]:
        async with self.engine.begin() as session:
            query = select(func.max(InterviewAnswerModel.question_order)).where(
                InterviewAnswerModel.interview_id == interview_id
            )
            result = await session.execute(query)
            return result.scalar()
