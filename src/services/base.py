from typing import TypeVar, Optional

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncEngine

from repositories.interview_repo import InterviewRepo
from repositories.pack_repo import PackRepo
from repositories.question_repo import QuestionRepo
from services.audio import AudioLambda, AudioFfmpeg
from services.interview import InterviewService, InterviewFinishService
from services.pack import PackService

T = TypeVar("T")

__services: dict[type, object] = {}


def register_services(bot: Bot, engine: AsyncEngine):
    global __services

    interview_repo = InterviewRepo(engine)
    pack_repo = PackRepo(engine)
    question_repo = QuestionRepo(engine)

    audio = AudioFfmpeg(bot)

    pack_service = PackService(pack_repo=pack_repo)
    __services[PackService] = pack_service

    interview_service = InterviewService(
        interview_repo=interview_repo, question_repo=question_repo
    )
    __services[InterviewService] = interview_service

    interview_finish_service = InterviewFinishService(
        interview_service=interview_service,
        pack_service=pack_service,
        audio_service=audio,
    )
    __services[InterviewFinishService] = interview_finish_service


def get_service(cls: T):
    service: Optional[T] = __services.get(cls)
    if not service:
        raise Exception(f"Service {cls} not initialized")

    return service
