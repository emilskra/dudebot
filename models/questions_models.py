from sqlalchemy import Column, String, ForeignKey
from models.base_models import IDMixin


class Pack(IDMixin):
    __tablename__ = "packs"

    name = Column(String)
    intro = Column(String)
    outro = Column(String)


class Questions(IDMixin):
    __tablename__ = "questions"

    pack = Column(ForeignKey("Pack", ondelete='CASCADE'), nullable=False, index=True)
    file_id = Column(String, nullable=False)
