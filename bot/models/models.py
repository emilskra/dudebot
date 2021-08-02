from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class IdMixin(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class BotTokenMixin(Base):
    __abstract__ = True
    token = Column(String)


class Pack(IdMixin, BotTokenMixin):
    __tablename__ = "packs"

    name = Column(String)
    questions = relationship("Question")
    intro = Column(String)
    outro = Column(String)


class Question(IdMixin, BotTokenMixin):
    __tablename__ = "questions"

    text = Column(String)


class PackQuestions(IdMixin, BotTokenMixin):
    __tablename__ = "pack_question"

    pack = Column(ForeignKey("Pack", ondelete='CASCADE'), nullable=False, index=True)
    question = Column(ForeignKey("Question", ondelete='CASCADE'), nullable=False, index=True)


class Answer(IdMixin, BotTokenMixin):
    __tablename__ = "answers"

    text = Column(String)


class QuestionAnswer(IdMixin, BotTokenMixin):
    __tablename__ = "question_answer"

    question = Column(ForeignKey("Question", ondelete='CASCADE'), nullable=False, index=True)
    answer = Column(ForeignKey("Answer", ondelete='CASCADE'), nullable=False, index=True)
