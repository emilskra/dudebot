from sqlalchemy.orm import Session

from db.session import get_db
from models.interview_models import InterviewState, Interview


class InterviewRepo(object):

    def __init__(self, db: Session):
        self.db = db

    async def create(self, pack_id: int) -> Interview:
        interview = Interview(
            pack_id=pack_id,
            state=InterviewState.started
        )

        await self.db.add(interview)
        await self.db.flush()
        return interview

    async def set_state(self, interview_id: int, state: InterviewState):
        pass

    @property
    async def answers(self):
        return []

    async def add_answer(self, interview_id: int, question_file_id: str, answer_file_id: str):
        pass


def get_interview_repo():
    db: Session = get_db()

    return InterviewRepo(
        db=db,
    )
