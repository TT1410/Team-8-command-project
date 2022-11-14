from typing import Optional, Generator
import pickle
import os

from .record import Record


class AddressBook:

    def add_record(self, record: Record) -> None:
        with open(self.filename, 'ab') as fh:
            pickle.dump(record, fh)

    def get_contact(self, name: str) -> Record | None:
        for contact in self.get_all_contacts():
            if name == contact.name.value:
                return contact

    def search_contacts(self, value: str) -> list[Record] | None:
        found_contacts = []

        for contact in self.get_all_contacts():
            if value in contact.name.value or any(value in str(phone.value) for phone in contact.phones):
                found_contacts.append(contact)

        if found_contacts:
            return found_contacts

    # Temporary command due to impossibility to change object in the file
    def change_contact(self, contact: Record, remove: bool = False) -> None:
        temporary_filename = os.path.join(self.root_package, 'old_contacts.dat')
        os.rename(self.filename, temporary_filename)

        self.filename = temporary_filename

        new_address_book = AddressBook()

        for record in self.get_all_contacts():
            if record.name.value == contact.name.value:
                if remove:
                    continue

                new_address_book.add_record(contact)

            else:
                new_address_book.add_record(record)

        os.remove(temporary_filename)

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
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return []

        with open(self.filename, 'rb') as file:

            while True:
                try:
                    yield pickle.load(file)
                except EOFError:
                    break

    def __getitem__(self, item: str) -> Record:
        for contact in self.get_all_contacts():
            if item == contact.name.value:
                return contact
        else:
            raise KeyError(item)

    def __repr__(self):
        return "AddressBook({})".format(', '.join([f"{k}={v}" for k, v in self.__dict__.items()]))
