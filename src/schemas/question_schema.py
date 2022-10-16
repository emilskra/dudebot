from schemas.base import BaseSchema


class Question(BaseSchema):
    id: int
    file_id: str
    sort_order: str

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
