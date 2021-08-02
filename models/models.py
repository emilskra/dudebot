from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class IdMixin(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class ChatIDMixin(Base):
    __abstract__ = True

    chat_id = Column(String, index=True)


class Pack(IdMixin):
    __tablename__ = "packs"

    name = Column(String)
    intro = Column(String)
    outro = Column(String)


class Question(IdMixin):
    __tablename__ = "questions"

    text = Column(String)


class PackQuestions(IdMixin):
    __tablename__ = "pack_questions"

    pack = Column(ForeignKey("Pack", ondelete='CASCADE'), nullable=False, index=True)
    question = Column(ForeignKey("Question", ondelete='CASCADE'), nullable=False, index=True)

