from sqlalchemy import Column, Integer, String
from db.session import Base


class IDMixin(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class ChatIDMixin(Base):
    __abstract__ = True
    chat_id = Column(String, index=True)

