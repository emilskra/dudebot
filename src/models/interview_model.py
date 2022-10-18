import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class InterviewModel(Base):
    __tablename__ = "interview"

    id: Column = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status: Column = Column(String)
    user_id: Column = Column(Integer)
    pack_id: Column = Column(Integer)


class InterviewAnswerModel(Base):
    __tablename__ = "interview_answer"

    id: Column = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id: Column = Column(UUID(as_uuid=True))
    user_id: Column = Column(Integer)
    question: Column = Column(String)
    question_order: Column = Column(Integer)
    answer: Column = Column(String)
