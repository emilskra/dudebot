from sqlalchemy import Column, String, Integer

from models.base import Base


class PackModel(Base):
    __tablename__ = "pack"

    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String)
    intro_file: Column = Column(String)
    outro_file: Column = Column(String)
