from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.interview_repo import get_interview_repo, InterviewRepo
from db.repositories.pack_repo import PackRepo, get_pack_repo
from models.interview_models import InterviewState, Interview
from schemas.interview_schema import InterviewSchema, InterviewUpdateSchema
from services.audio import get_audio, Audio
from services.exceptions import InterviewNotFound, EmptyInterview, QuestionNotFound


class InterviewService(object):

    interview = None

    def __init__(
            self,
            user_id: int,
            interview_repo: InterviewRepo,
            pack_repo: PackRepo,
            audio: Audio,
    ):
        self.user_id = user_id
        self.interview_repo = interview_repo
        self.pack_repo = pack_repo
        self.audio = audio

    async def start(self, pack_id: int):
        interview_data = InterviewSchema(
            user_id=self.user_id,
            pack=pack_id,
        )
        self.interview = await self.interview_repo.update_or_create(interview_data)

    async def get_next_question(self, answer_file_id: str = None) -> str:
        interview = await self._get_interview()
        if answer_file_id:
            await self._save_answer(answer_file_id)

        question = await self.pack_repo.get_question(
            pack_id=interview.pack,
            question_number=interview.question + 1,
        )
        if not question:
            raise QuestionNotFound

        update_data = InterviewUpdateSchema(
            state=InterviewState.started,
            question=question.sort_order
        )
        await self.interview_repo.update(interview.id, update_data)

        return question.file_id

    @asynccontextmanager
    async def finish(self) -> str:
        await self._get_interview()
        file_ids: list[str] = await self._get_file_ids()
        finish_file = await self.audio.get_finish_file(file_ids)
        try:
            yield finish_file
        finally:
            await self._set_finish()
            await self.audio.clear(file_ids)

    async def _get_interview(self) -> Interview:
        self.interview = await self.interview_repo.get_user_active_interview(self.user_id)
        if not self.interview:
            raise InterviewNotFound

        return self.interview

    async def _save_answer(self, answer_file_id: str) -> None:
        question = await self.pack_repo.get_question(
            self.interview.pack,
            self.interview.question,
        )
        if not question:
            raise QuestionNotFound

        await self.interview_repo.add_answer(
            interview_id=self.interview.id,
            question_file_id=question.file_id,
            answer_file_id=answer_file_id,
        )

    async def _get_file_ids(self) -> list[str]:
        files_ids = []

        pack = await self.pack_repo.get(self.interview.pack)
        intro = pack.intro
        if intro:
            files_ids.append(intro)

        answers = await self.interview_repo.get_answers(self.interview.id)
        if not answers:
            raise EmptyInterview

        for question_answer in answers:
            files_ids.append(question_answer.question_file_id)
            files_ids.append(question_answer.answer_file_id)

        outro = pack.outro
        if outro:
            files_ids.append(outro)

        return files_ids

    async def _set_finish(self) -> None:
        update_data = InterviewUpdateSchema(
            state=InterviewState.finish,
            question=0
        )
        await self.interview_repo.update(self.interview.id, update_data)


async def get_interview_service(user_id: int, db: AsyncSession) -> InterviewService:
    interview_repo = await get_interview_repo(db)
    pack_repo = await get_pack_repo(db)
    audio_service = get_audio()

    return InterviewService(
        user_id=user_id,
        interview_repo=interview_repo,
        pack_repo=pack_repo,
        audio=audio_service,
    )
