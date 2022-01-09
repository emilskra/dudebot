from bson import ObjectId
from pydantic import BaseModel, Field

from src.schemas.base import PyObjectId


class Question(BaseModel):
    file_id: str
    sort_order: str

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Pack(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    intro: str
    outro: str
    questions: list[Question] = []

    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
