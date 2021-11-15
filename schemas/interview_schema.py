from pydantic import BaseModel

from models.interview_models import InterviewState


class InterviewSchema(BaseModel):

    state: InterviewState
    question: int

    class Config:   # noqa: WPS431
        orm_mode = True
        use_enum_values = True
