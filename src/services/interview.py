import io

from repositories.question_repo import QuestionRepo
from schemas.question_schema import Question
from services.pack import PackService
from repositories.interview_repo import InterviewRepo
from schemas.interview_schema import (
    InterviewUpdate,
    InterviewState,
    InterviewCreate,
    InterviewAnswer,
    Interview,
)
from services.audio import BaseAudio
from services.exceptions import EmptyInterview, InterviewNotFound, QuestionNotFound


class InterviewService:
    def __init__(self, interview_repo: InterviewRepo, question_repo: QuestionRepo):
        self.question_repo = question_repo
        self.interview_repo = interview_repo

    async def start_interview(self, pack_id: int, user_id: int):

        await self.set_interview_finish(user_id)

        interview_data = InterviewCreate(
            user_id=user_id, pack_id=pack_id, status=InterviewState.started
        )
        await self.interview_repo.create(interview_data)

    async def get_user_active_interview(self, user_id: int) -> Interview:  # TODO: cache
        user_interview = await self.interview_repo.get_user_active_interview(user_id)
        if not user_interview:
            raise InterviewNotFound

        return Interview.from_orm(user_interview)

    async def get_next_question(self, user_id: int) -> Question:
        user_interview = await self.get_user_active_interview(user_id)

        last_question_order = (
            await self.question_repo.get_interview_last_question_order(
                user_interview.id
            )
        )
        sort_order = last_question_order + 1 if last_question_order is not None else 0
        question = await self.question_repo.get_pack_question(
            pack_id=user_interview.pack_id,
            sort_order=sort_order,
        )
        if not question:
            raise QuestionNotFound

        return Question.from_orm(question)

    async def save_answer(self, user_id: int, answer_file: str):
        user_interview = await self.get_user_active_interview(user_id)

        next_question = await self.get_next_question(user_id)

        interview_answer = InterviewAnswer(
            user_id=user_id,
            answer=answer_file,
            interview_id=user_interview.id,
            question=next_question.file_id,
            question_order=next_question.sort_order,
        )
        await self.interview_repo.add_interview_answer(interview_answer)

    async def set_interview_finish(self, user_id: int) -> None:
        update_data = InterviewUpdate(
            status=InterviewState.finish,
        )
        await self.interview_repo.update(user_id, update_data)

    async def get_user_interview_answers(self, user_id: int) -> list[InterviewAnswer]:
        user_interview = await self.get_user_active_interview(user_id)
        answers = await self.interview_repo.get_interview_answers(user_interview.id)
        if not answers:
            raise EmptyInterview

        return [
            InterviewAnswer.from_orm(interview_answer) for interview_answer in answers
        ]


class InterviewFinishService:
    def __init__(
        self,
        interview_service: InterviewService,
        pack_service: PackService,
        audio_service: BaseAudio,
    ):
        self.interview_service = interview_service
        self.pack_service = pack_service
        self.audio_service = audio_service

    async def get_interview_finish_file(self, user_id: int) -> io.BytesIO:
        file_ids: list[str] = await self.get_user_interview_files(user_id)

        finish_file_name = f"{user_id}.ogg"
        finish_file = await self.audio_service.join_files(file_ids, finish_file_name)

        return finish_file

    async def get_user_interview_files(self, user_id: int) -> list[str]:
        files_ids = []

        user_active_interview = await self.interview_service.get_user_active_interview(
            user_id
        )
        pack = await self.pack_service.get_pack(user_active_interview.pack_id)

        answers = await self.interview_service.get_user_interview_answers(user_id)
        if not answers:
            raise EmptyInterview

        if pack.intro_file:
            files_ids.append(pack.intro_file)

        for question_answer in answers:
            files_ids.append(question_answer.question)
            files_ids.append(question_answer.answer)

        if pack.outro_file:
            files_ids.append(pack.outro_file)

        return files_ids
