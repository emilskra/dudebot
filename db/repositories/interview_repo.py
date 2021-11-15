from sqlalchemy import select, update
from sqlalchemy.orm import Session

from db.session import get_db
from models.interview_models import InterviewState, Interview, Answers
from schemas.interview_schema import InterviewSchema


class InterviewRepo(object):

    def __init__(self, db: Session):
        self.db = db

    async def get(self, interview_id: int) -> Interview:
        return await self.db.get(Interview, interview_id)

    async def create(self, user_id: int, pack_id: int) -> Interview:
        interview = Interview(
            user_id=user_id,
            pack_id=pack_id,
            state=InterviewState.started,
            question=0,
        )

        await self.db.add(interview)
        await self.db.flush()
        return interview

    async def get_user_active_interview(self, user_id: int):
        interview = await self.db.execute(
            select(
                Interview,
            ).where(
                Interview.user_id == user_id,
                Interview.state == InterviewState.started,
            )
        )

        return interview

    async def update(self, interview: Interview, update_data: InterviewSchema):
        await self.db.execute(
            update(
                Interview,
            ).values(
                **update_data.dict(),
            ).where(
                id == interview
            )
        )

    async def set_state(self, interview_id: int, state: InterviewState):
        pass

    async def get_answers(self, interview: Interview) -> list[Answers]:
        answers = await self.db.execute(
            select(
                Answers,
            ).where(
                Answers.interview == interview,
            )
        )

        return answers

    async def add_answer(
            self,
            interview: Interview,
            question_file_id: str,
            answer_file_id: str,
    ):
        answer = Answers(
            interview=interview,
            question_file_id=question_file_id,
            answer_file_id=answer_file_id
        )
        await self.db.add(answer)
        await self.db.flush()

        return answer


def get_interview_repo():
    db: Session = get_db()

    return InterviewRepo(
        db=db,
    )
