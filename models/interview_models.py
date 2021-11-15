import enum

from sqlalchemy import Enum, Column, String, ForeignKey
from models.base_models import IDMixin, ChatIDMixin


class InterviewState(str, enum.Enum):
    started = "started"
    finish = "finish"


class Interview(IDMixin, ChatIDMixin):
    __tablename__ = "interviews"

    pack = Column(ForeignKey("Pack", ondelete='CASCADE'), nullable=False, index=True)
    state = Column(Enum(InterviewState))


class Answers(IDMixin):
    __tablename__ = "answers"

    interview = Column(ForeignKey("Interview", ondelete='CASCADE'), nullable=False, index=True)
    question_file_id = Column(String, nullable=False)
    answer_file_id = Column(String, nullable=False)
