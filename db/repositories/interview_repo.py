from typing import Union

from sqlalchemy import select, update

from db.session import async_session
from models.interview_models import InterviewState, Interview, Answers
from schemas.interview_schema import InterviewSchema, InterviewUpdateSchema


class InterviewRepo(object):

    async def update_or_create(self, interview: InterviewSchema) -> Interview:
        async with async_session.begin() as session:
            interview_db = await session.execute(
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
        async with async_session.begin() as session:
            return await session.get(Interview, interview_id)

    async def create(self, interview: InterviewSchema) -> Interview:
        async with async_session.begin() as session:
            interview = Interview(
                **interview.dict(),
            )

            session.add(interview)
            await session.commit()
            return interview

    async def get_user_active_interview(self, user_id: int):
        async with async_session.begin() as session:
            interview = await session.execute(
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
        async with async_session.begin() as session:
            await session.execute(
                update(
                    Interview,
                ).values(
                    **update_data.dict(),
                ).where(
                    Interview.id == interview_id,
                )
            )
            await session.commit()

    async def get_answers(self, interview_id: int) -> list[Answers]:
        async with async_session.begin() as session:
            answers = await session.execute(
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
        async with async_session.begin() as session:
            answer = Answers(
                interview=interview_id,
                question_file_id=question_file_id,
                answer_file_id=answer_file_id
            )
            session.add(answer)
            return answer


async def get_interview_repo():
    return InterviewRepo()
