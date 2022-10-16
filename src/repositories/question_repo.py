import ydb

from schemas.question_schema import Question


class QuestionRepo:

    def __init__(self, session_pool: ydb.aio.SessionPool):
        self.session_pool = session_pool

    async def get_pack_questions(self, pack_id: int) -> list[Question]:
        ...

    async def get_user_next_question(self, user_id: int) -> Question:
        ...
