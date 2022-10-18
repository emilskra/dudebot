from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:  # noqa: WPS431
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
