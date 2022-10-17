from typing import Optional

from schemas.base import BaseSchema


class Pack(BaseSchema):
    id: int
    name: str
    intro_file: Optional[str]
    outro_file: Optional[str]

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True


class PackGet(BaseSchema):
    id: int
    name: str
