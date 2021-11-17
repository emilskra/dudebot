from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_models import IDMixin


class Pack(IDMixin):
    __tablename__ = "packs"

    name = Column(String)
    intro = Column(String)
    outro = Column(String)


class Question(IDMixin):
    __tablename__ = "questions"

    pack = Column(ForeignKey("packs.id", ondelete='CASCADE'), nullable=False, index=True)
    file_id = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
