from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from services.db.base import Base


class ModelNotes(Base):
    """Notes"""
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    note = Column(String)
    tags = Column(String, primary_key=True)  # text array
