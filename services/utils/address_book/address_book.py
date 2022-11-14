from typing import Optional, Generator
import json

from sqlalchemy import (
    select,
)

from services.db import (
    DBSession,
    models,
)
from .record import Record
from .phone import Phone


class AddressBook(DBSession):

    def get_contact(self, name: str) -> Record | None:
        with self.db_session() as session:
            contact = session.execute(
                select(models.ModelContacts)
                .where(models.ModelContacts.name == name)
            ).scalar()

            return self.__record_from_models_to_class(contact)

    def search_contacts(self, value: str) -> list[Record] | None:
        found_contacts = []

        for contact in self.get_all_contacts():
            if value in contact.name.value or any(value in str(phone.value) for phone in contact.phones):
                found_contacts.append(contact)

        if found_contacts:
            return found_contacts

    def iterator(self, count: Optional[int] = None) -> 'Generator[list[Record]]':
        count = count if count else "inf"

        records = []

        for record in self.get_all_contacts():
            records.append(record)

            if len(records) >= count:
                yield records
                records = []

        if records:
            yield records

    def get_all_contacts(self) -> 'Generator[Record]':
        with self.db_session() as session:
            records = session.execute(
                select(models.ModelContacts)
            ).scalars()

            for record in records:
                yield self.__record_from_models_to_class(record)

    def __getitem__(self, item: str) -> Record:
        record = self.get_contact(item)

        if not record:
            raise KeyError(item)

        return record

    @classmethod
    def __record_from_models_to_class(cls, record: models.ModelContacts) -> Optional[Record]:
        if not record:
            return

        contact = Record(
            name=record.name,
            birthday=record.birthday.isoformat(),
            address=record.address,
            email=record.email,
            contact_id=record.id
        )

        contact.phones = [Phone(str(x)) for x in json.loads(record.phones)]

        return contact
