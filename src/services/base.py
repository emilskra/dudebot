from typing import TypeVar, Optional

from db.session import get_session_pool
from repositories.interview_repo import InterviewRepo
from repositories.pack_repo import PackRepo
from repositories.question_repo import QuestionRepo
from services.audio import AudioLambda
from services.interview import InterviewService, InterviewFinishService
from services.pack import PackService
from services.question import QuestionService

T = TypeVar("T")

__services: dict[type, object] = {}


async def register_services():
    global __services
    db_session_pool = await get_session_pool()

    interview_repo = InterviewRepo(db_session_pool)
    pack_repo = PackRepo(db_session_pool)
    question_repo = QuestionRepo(db_session_pool)

    audio = AudioLambda()

    pack_service = PackService(pack_repo=pack_repo)
    __services[PackService] = pack_service

    questions_service = QuestionService(question_repo=question_repo)
    __services[QuestionService] = questions_service

    interview_service = InterviewService(interview_repo=interview_repo)
    __services[InterviewService] = interview_service

    interview_finish_service = InterviewFinishService(
        interview_service=interview_service,
        pack_service=pack_service,
        audio_service=audio,
    )
    __services[InterviewFinishService] = interview_finish_service


def get_service(cls: T):
    service: Optional[T] = __services.get(cls)
    return service
