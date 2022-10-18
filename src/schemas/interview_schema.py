import enum
import uuid

from schemas.base import BaseSchema


class InterviewState(str, enum.Enum):
    started = "started"
    finish = "finish"


class Interview(BaseSchema):
    id: uuid.UUID
    status: InterviewState
    user_id: int
    pack_id: int

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True


class InterviewCreate(BaseSchema):
    status: InterviewState
    user_id: int
    pack_id: int


class InterviewUpdate(BaseSchema):
    status: InterviewState


class InterviewAnswer(BaseSchema):
    user_id: int
    interview_id: uuid.UUID
    answer: str
    question: str
    question_order: int

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True
