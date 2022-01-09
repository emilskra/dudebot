import enum

from bson import ObjectId
from pydantic import BaseModel, Field

from src.schemas.answer_schema import Answer
from src.schemas.base import PyObjectId


class InterviewState(str, enum.Enum):
    started = "started"
    finish = "finish"


class Interview(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: int
    pack: PyObjectId
    state: InterviewState = InterviewState.started
    question: int = 0
    answers: list[Answer] = []

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        use_enum_values = True


class InterviewUpdate(BaseModel):
    state: InterviewState
    question: int
    answers: list[Answer] = []

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        use_enum_values = True
