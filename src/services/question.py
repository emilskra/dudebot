
from repositories.question_repo import QuestionRepo
from services.exceptions import QuestionNotFound


class QuestionService:

    def __init__(
            self,
            question_repo: QuestionRepo,
    ):
        self.question_repo = question_repo

    async def get_next_question(self, user_id: int, ) -> str:
        question = await self.question_repo.get_user_next_question(user_id=user_id)
        if not question:
            raise QuestionNotFound

        return question.file_id
