from typing import Union

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_session
from models.interview_models import InterviewState, Interview, Answers
from schemas.interview_schema import InterviewSchema, InterviewUpdateSchema


class InterviewRepo(object):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_or_create(self, interview: InterviewSchema) -> Interview:
        interview_db = await self.db.execute(
            select(
                Interview.id,
                Interview.user_id,
                Interview.pack,
                Interview.question,
                Interview.state,
            ).where(
                Interview.user_id == interview.user_id,
            ),
        )
        interview_db = interview_db.first()
        if interview_db:
            interview_db = await self.update(interview_db.id, interview)
        else:
            interview_db = await self.create(interview)

        return interview_db

    async def get(self, interview_id: int) -> Interview:
        return await self.db.get(Interview, interview_id)

    async def create(self, interview: InterviewSchema) -> Interview:
        interview = Interview(
            **interview.dict(),
        )

        self.db.add(interview)
        await self.db.commit()
        return interview

    async def get_user_active_interview(self, user_id: int):
        interview = await self.db.execute(
            select(
                Interview.id,
                Interview.user_id,
                Interview.pack,
                Interview.question,
                Interview.state,
            ).where(
                Interview.user_id == user_id,
                Interview.state == InterviewState.started,
            ),
        )

        return interview.first()

    async def update(
            self,
            interview_id: int,
            update_data: Union[InterviewSchema, InterviewUpdateSchema]
    ):
        await self.db.execute(
            update(
                Interview,
            ).values(
                **update_data.dict(),
            ).where(
                Interview.id == interview_id,
            )
        )
        await self.db.commit()

    async def get_answers(self, interview_id: int) -> list[Answers]:
        answers = await self.db.execute(
            select(
                Answers.question_file_id,
                Answers.answer_file_id,
            ).where(
                Answers.interview == interview_id,
            )
        )

        return answers.all()

    async def add_answer(
            self,
            interview_id: int,
            question_file_id: str,
            answer_file_id: str,
    ):
        answer = Answers(
            interview=interview_id,
            question_file_id=question_file_id,
            answer_file_id=answer_file_id
        )
        self.db.add(answer)
        await self.db.commit()
        return answer


async def get_interview_repo(db: AsyncSession):
    return InterviewRepo(db)
