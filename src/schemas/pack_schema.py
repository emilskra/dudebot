from typing import Optional

from schemas.base import BaseSchema


class Pack(BaseSchema):
    id: int
    name: str
    intro_file: Optional[str]
    outro_file: Optional[str]
