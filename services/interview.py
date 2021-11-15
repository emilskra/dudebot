from db.repositories.interview_repo import get_interview_repo, InterviewRepo
from db.repositories.pack_repo import PackRepo, get_pack_repo
from models.interview_models import InterviewState
from schemas.interview_schema import InterviewSchema
from services.exceptions import QuestionsEnded, InterviewNotFound


class Interview(object):

    def __init__(
            self,
            user_id: int,
            interview_repo: InterviewRepo,
            pack_repo: PackRepo,
    ):
        self.user_id = user_id
        self.interview_repo = interview_repo
        self.pack_repo = pack_repo

    async def interview(self):
        interview = await self.interview_repo.get_user_active_interview(self.user_id)
        if not interview:
            raise InterviewNotFound

        return interview

    async def start(self, pack_id: int) -> None:
        await self.interview_repo.create(
            user_id=self.user_id,
            pack_id=pack_id
        )

    async def get_next_question(self) -> str:
        interview = await self.interview()
        question = await self.pack_repo.get_question(interview.pack, interview.question + 1)
        if not question:
            raise QuestionsEnded

        return question

    async def save_answer(self, answer_file_id: str) -> None:
        interview = await self.interview()
        question = await self.pack_repo.get_question(interview.pack, interview.question)
        if not question:
            raise QuestionsEnded

        await self.interview_repo.add_answer(
            interview=interview,
            question_file_id=question.file_id,
            answer_file_id=answer_file_id
        )

        update_data = InterviewSchema(
            state=InterviewState.started,
            question=question + 1
        )
        await self.interview_repo.update(interview, update_data)

    async def get_file_ids(self) -> list[str]:
        interview = await self.interview()

        files_ids = []
        pack = await self.pack_repo.get(interview.pack)
        intro = pack.intro
        if intro:
            files_ids.append(intro)

        answers = await self.interview_repo.get_answers(interview)
        for question_answer in answers:
            files_ids.append(question_answer.question_file_id)
            files_ids.append(question_answer.answer_file_id)

        outro = pack.outro
        if outro:
            files_ids.append(outro)

        return files_ids

    async def end(self):
        interview = await self.interview()

        update_data = InterviewSchema(
            state=InterviewState.finish,
            question=0
        )
        await self.interview_repo.update(interview, update_data)


def get_interview_service(user_id: int):
    interview_repo = get_interview_repo()
    pack_repo = get_pack_repo()

    return Interview(
        interview_repo=interview_repo,
        pack_repo=pack_repo,
        user_id=user_id,
    )
