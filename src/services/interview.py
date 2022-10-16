import io

from services.pack import PackService
from repositories.interview_repo import InterviewRepo
from schemas.interview_schema import InterviewUpdate, InterviewState, InterviewCreate
from services.audio import BaseAudio
from services.exceptions import EmptyInterview


class InterviewService:

    def __init__(self, interview_repo: InterviewRepo):
        self.interview_repo = interview_repo

    async def start_interview(self, pack_id: int, user_id: int):

        await self.set_interview_finish(user_id)

        interview_data = InterviewCreate(user_id=user_id, pack=pack_id, status=InterviewState.started)
        return await self.interview_repo.create(interview_data)

    async def save_answer(self, user_id: int, answer_file: str):
        await self.interview_repo.add_interview_answer(user_id=user_id, answer_file=answer_file)

    async def set_interview_finish(self, user_id: int) -> None:
        update_data = InterviewUpdate(
            state=InterviewState.finish,
        )
        await self.interview_repo.update(user_id, update_data)

    async def get_user_interview_answers(self, user_id: int):
        user_interview = await self.interview_repo.get_user_active_interview(user_id)
        return await self.interview_repo.get_interview_answers(user_interview.id)


class InterviewFinishService:

    def __init__(self, interview_service: InterviewService, pack_service: PackService, audio_service: BaseAudio):
        self.interview_service = interview_service
        self.pack_service = pack_service
        self.audio_service = audio_service

    async def get_interview_finish_file(self, user_id: int) -> io.BytesIO:
        file_ids: list[str] = await self._get_user_interview_files(user_id)
        finish_file_name = f"{user_id}.ogg"
        finish_file = await self.audio_service.join_files(file_ids, finish_file_name)
        return finish_file

    async def _get_user_interview_files(self, user_id: int) -> list[str]:
        files_ids = []

        pack = await self.pack_service.get_user_pack(user_id)
        answers = await self.interview_service.get_user_interview_answers(user_id)
        if not answers:
            raise EmptyInterview

        if pack.intro:
            files_ids.append(pack.intro)

        for question_answer in answers:
            files_ids.append(question_answer.question_file_id)
            files_ids.append(question_answer.answer_file_id)

        if pack.outro:
            files_ids.append(pack.outro)

        return files_ids
