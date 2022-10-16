import uuid

import ydb

from schemas.interview_schema import Interview, InterviewUpdate, InterviewState, InterviewCreate, InterviewAnswer


class InterviewRepo:

    def __init__(self, session_pool: ydb.aio.SessionPool):
        self.session_pool = session_pool

    async def create(self, interview: InterviewCreate) -> None:
        async def execute(session):
            query = """
                DECLARE $id AS String;
                DECLARE $user_id AS Int32;
                DECLARE $pack_id AS Int32;
                DECLARE $status AS String;
                INSERT INTO interviews (id, pack_id, user_id, status)
                VALUES ($id, $user_id, $pack_id, $status);
             """
            prepared_query = await session.prepare(query)
            await session.transaction().execute(
                prepared_query,
                parameters={
                    "id": str(uuid.uuid4()).encode(),
                    "$user_id": Interview.user_id,
                    "$pack_id": interview.pack_id,
                    "$status": Interview.status.encode(),
                },
                commit_tx=True,
            )

        await self.session_pool.retry_operation(execute)

    async def update(
            self,
            user_id: int,
            interview: InterviewUpdate,
    ):

        async def execute(session):
            query = """
                DECLARE $user_id AS Int32;
                DECLARE $status AS String;
                DECLARE $active_status AS String;
                UPDATE interviews
                SET status = $status
                WHERE user_id = $user_id and status = $active_status
            """
            prepared_query = await session.prepare(query)
            await session.transaction().execute(
                prepared_query,
                parameters={
                    "id": str(uuid.uuid4()).encode(),
                    "$user_id": user_id,
                    "$status": interview.status.encode(),
                    "$active_status": InterviewState.started.encode(),
                },
                commit_tx=True,
            )

        await self.session_pool.retry_operation(execute)

    async def get_user_active_interview(self, user_id: int) -> Interview:
        ...

    async def get_last_interview_answer(self, interview_id: str) -> InterviewAnswer:
        ...

    async def add_interview_answer(self, user_id: int, answer_file: str):
        user_interview = await self.get_user_active_interview(user_id)
        last_interview_answer = await self.get_last_interview_answer(user_interview.id)

        async def execute(session):
            query = """
                DECLARE $id AS String;
                DECLARE $user_id AS Int32;
                DECLARE $answer_file AS String;
                DECLARE $interview_id AS Int32;
                DECLARE $question_order AS Int32;
                INSERT INTO interview_answer (id, interview_id, question_order, user_id, answer)
                VALUES ($id, $interview_id, $question_order, $user_id, $answer_file);
            """
            prepared_query = await session.prepare(query)
            await session.transaction().execute(
                prepared_query,
                parameters={
                    "id": str(uuid.uuid4()).encode(),
                    "$user_id": user_id,
                    "$answer_file": answer_file.encode(),
                    "$interview_id": user_interview.id,
                    "$question_order": last_interview_answer.question_order + 1,
                },
                commit_tx=True,
            )

        await self.session_pool.retry_operation(execute)

    async def get_interview_answers(self, interview_id: str) -> list[InterviewAnswer]:
        ...
