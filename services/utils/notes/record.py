import json
from typing import Optional

from sqlalchemy import (
    delete,
    update,
)

from services.db import (
    DBSession,
    models,
)
from .text import Text
from .tag import Tag


class Record(DBSession):
    def __init__(self,
                 text: str,
                 tags: Optional[list[str]] = None,
                 id: Optional[int] = None) -> None:
        self.text: Text = Text(text)
        self.tags: list[Tag] = [Tag(tag) for tag in tags] if tags else []
        self.id: Optional[int] = id

        if not self.id:
            self.__save_record()

    def __save_record(self) -> None:
        str_tags = json.dumps([x.value for x in self.tags])

        with self.db_session() as session:
            record = session.merge(models.ModelNotes(note=self.text.value, tags=str_tags))
            session.commit()

            self.id = record.id

    def replace_text(self, new_text: str) -> None:
        self.text = new_text

        with self.db_session() as session:
            session.execute(
                update(models.ModelNotes)
                .where(models.ModelNotes.id == self.id)
                .values(note=self.text)
            )
            session.commit()

    def add_tags(self, new_tags: list[str]) -> None:
        self.tags.extend([Tag(tag) for tag in new_tags])

        str_tags = json.dumps([x.value for x in self.tags])

        with self.db_session() as session:
            session.execute(
                update(models.ModelNotes)
                .where(models.ModelNotes.id == self.id)
                .values(tags=str_tags)
            )
            session.commit()

    def remove_record(self) -> None:
        with self.db_session() as session:
            session.execute(
                delete(models.ModelNotes)
                .where(models.ModelNotes.id == self.id)
            )
            session.commit()

    def __repr__(self):
        return "Record({})".format(', '.join([f"{k}={v}" for k, v in self.__dict__.items()]))
