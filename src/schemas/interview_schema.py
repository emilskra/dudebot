import enum

from schemas.base import BaseSchema


class InterviewState(str, enum.Enum):
    started = "started"
    finish = "finish"


class Interview(BaseSchema):
    id: str
    status: InterviewState
    user_id: int
    pack_id: int


class InterviewCreate(BaseSchema):
    status: InterviewState
    user_id: int
    pack_id: int


class InterviewUpdate(BaseSchema):
    status: InterviewState


class InterviewAnswer(BaseSchema):
    id: str
    answer: str
    interview_id: int
    question: int
    question_order: int
    user_id: int
