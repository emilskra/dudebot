from sqlalchemy import Column, Integer, String

from models.base import Base


class QuestionModel(Base):
    __tablename__ = "question"

    id: Column = Column(Integer, primary_key=True)
    pack_id: Column = Column(Integer)
    file_id: Column = Column(String)
    sort_order: Column = Column(Integer)
