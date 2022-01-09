from pydantic import BaseModel


class Answer(BaseModel):
    question_file_id: int
    answer_file_id: int

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
