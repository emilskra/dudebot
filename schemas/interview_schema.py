from pydantic import BaseModel

from models.interview_models import InterviewState


class InterviewSchema(BaseModel):
    user_id: int
    pack: int
    state: InterviewState = InterviewState.started
    question: int = 0

    class Config:  # noqa: WPS431
        orm_mode = True
        use_enum_values = True


class InterviewUpdateSchema(BaseModel):
    state: InterviewState
    question: int

    class Config:  # noqa: WPS431
        orm_mode = True
        use_enum_values = True
