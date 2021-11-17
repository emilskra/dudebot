import enum

from sqlalchemy import Enum, Column, String, Integer, ForeignKey
from models.base_models import IDMixin, UserIDMixin


class InterviewState(str, enum.Enum):
    started = "started"
    finish = "finish"


class Interview(IDMixin, UserIDMixin):
    __tablename__ = "interviews"

    pack = Column(ForeignKey("packs.id", ondelete='CASCADE'), nullable=False, index=False)
    state = Column(Enum(InterviewState))
    question = Column(Integer, nullable=True)


class Answers(IDMixin):
    __tablename__ = "answers"

    interview = Column(ForeignKey("interviews.id", ondelete='CASCADE'), nullable=False, index=True)
    question_file_id = Column(String, nullable=False)
    answer_file_id = Column(String, nullable=False)
