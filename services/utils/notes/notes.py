import json
from typing import Optional, Generator

from sqlalchemy import (
    select,
)

from services.db import (
    DBSession,
    models,
)
from .record import Record


class Notes(DBSession):
    def search_notes_by_text(self, contains_text: str) -> list[Record]:
        with self.db_session() as session:
            records = session.execute(
                select(models.ModelNotes)
                .where(models.ModelNotes.note.like(f"%{contains_text}%"))
            ).scalars()

            return [self.__record_from_models_to_class(x) for x in records]

    def search_notes_by_tags(self, tags: list[str]) -> list[Record]:
        notes = []

        for note in self.get_all_records():
            if any(x.value in tags for x in note.tags):
                notes.append(note)

        return notes

    def get_all_records(self) -> 'Generator[Record]':
        with self.db_session() as session:
            records = session.execute(
                select(models.ModelNotes)
            ).scalars()

            for record in records:
                yield self.__record_from_models_to_class(record)

    def search_notes_by_id(self, _id: int) -> Record:
        with self.db_session() as session:
            record = session.execute(
                select(models.ModelNotes)
                .where(models.ModelNotes.id == _id)
            ).scalar()

            if not record:
                raise IndexError

            return record

    @staticmethod
    def __record_from_models_to_class(record: models.ModelNotes) -> Record:
        return Record(text=record.note, tags=json.loads(record.tags), _id=record.id)
