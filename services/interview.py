from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from db.repositories.interview_repo import get_interview_repo, InterviewRepo
from db.repositories.pack_repo import PackRepo, get_pack_repo
from models.interview_models import InterviewState


class QuestionsEnded(Exception):
    ...


@dataclass
class QuestionAnswer:
    question: str
    answer: str


class Interview:

    def __init__(
            self,
            chat_id: int,
            pack_id: int,
            interview_repo: InterviewRepo,
            pack_repo: PackRepo,
    ):
        self.chat_id = chat_id
        self.pack_id = pack_id
        self.interview_repo = interview_repo
        self.pack_repo = pack_repo
        self.interview = await self.interview_repo.create(self.pack_id)

    async def get_next_question(self) -> str:
        pack_questions = await self.pack_repo.get_pack_questions(self.pack_id)
        answers = await self.interview_repo.answers

        if len(pack_questions) == len(answers):
            raise QuestionsEnded

        return pack_questions[len(answers)]

    async def save_answer(self, answer_file_id: str) -> None:
        await self.interview_repo.add_answer(
            interview_id=self.interview.id,
            question_file_id='',
            answer_file_id=answer_file_id
        )

    async def get_file_ids(self) -> list[str]:

        files_ids = []
        pack = await self.pack_repo.get(self.pack_id)
        intro = pack.intro
        if intro:
            files_ids.append(intro)

        answers = await self.interview_repo.answers
        for question_answer in answers:
            files_ids.append(question_answer.question_file_id)
            files_ids.append(question_answer.answer_file_id)

        outro = pack.outro
        if outro:
            files_ids.append(outro)

        return files_ids


def get_interview_service(chat_id: int, pack_id: int):
    interview_repo = get_interview_repo()
    pack_repo = get_pack_repo()

    return Interview(
        interview_repo=interview_repo,
        pack_repo=pack_repo,
        chat_id=chat_id,
        pack_id=pack_id,
    )
