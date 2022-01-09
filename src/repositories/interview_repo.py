import motor.motor_asyncio as motor_async

from src.schemas.answer_schema import Answer
from src.schemas.base import PyObjectId
from src.schemas.interview_schema import Interview, InterviewUpdate, InterviewState


class InterviewRepo(object):

    def __init__(self, db: motor_async.AsyncIOMotorClient):
        self.db = db
        self.document = db["interviews"]

    async def get(self, interview_id: PyObjectId) -> Interview:
        interview = await self.document.find_one({"_id": interview_id})
        return Interview(**interview)

    async def create(self, interview: Interview) -> Interview:
        new_interview = await self.document.insert_one(interview)
        created = await self.document.find_one({"_id": new_interview.inserted_id})
        return Interview(**created)

    async def get_user_active_interview(self, user_id: int):
        active_interview = await self.document.find_one({
            "user_id": user_id,
            "status": InterviewState.started,
        })
        return active_interview

    async def update(
            self,
            interview_id: PyObjectId,
            interview: InterviewUpdate
    ) -> Interview:
        update_result = await self.document.update_one({"_id": interview_id}, {"$set": interview})
        return Interview(**update_result)

    async def add_answer(
            self,
            interview_id: PyObjectId,
            question_file_id: str,
            answer_file_id: str,
    ):
        interview = await self.get(interview_id)
        interview_update = InterviewUpdate(**interview.dict())
        answer = Answer(
            question_file_id=question_file_id,
            answer_file_id=answer_file_id
        )

        interview_update.answers.append(answer)
        await self.update(interview_id, interview_update)


async def get_interview_repo(db: motor_async):
    return InterviewRepo(db)
