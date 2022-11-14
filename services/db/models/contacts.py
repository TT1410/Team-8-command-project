from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from services.db.base import Base


class ModelNotes(Base):
    """Notes"""
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    note = Column(String, unique=True)
    tags = Column(String, index=True)  # text array

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return ("ModelNotes({})".format(
            ', '.join([f"{k}={v!r}" for k, v in filter(lambda x: not x[0].startswith("_"), self.__dict__.items())]))
        )
