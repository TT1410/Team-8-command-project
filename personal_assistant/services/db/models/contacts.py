from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
)

from personal_assistant.services.db.base import Base


class ModelContacts(Base):
    """Contacts table"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    phones = Column(String, index=True)  # text array
    birthday = Column(Date)
    address = Column(String)
    email = Column(String)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return ("ModelContacts({})".format(
            ', '.join([f"{k}={v!r}" for k, v in filter(lambda x: not x[0].startswith("_"), self.__dict__.items())]))
        )
