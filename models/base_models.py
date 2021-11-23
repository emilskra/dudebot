from sqlalchemy import Column, Integer, String
from db.session import Base


class IDMixin(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class UserIDMixin(Base):
    __abstract__ = True
    user_id = Column(Integer, index=True, nullable=False)

