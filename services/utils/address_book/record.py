import json
from typing import Optional
from datetime import date

from sqlalchemy import (
    delete,
    update,
    exc,
)

from services.db import (
    DBSession,
    models,
)
from .name import Name
from .phone import Phone
from .birthday import Birthday
from .address import Address
from .email import Email


class Record(DBSession):
    def __init__(self,
                 name: str,
                 phone: Optional[str] = None,
                 birthday: Optional[str] = None,
                 address: Optional[str] = None,
                 email: Optional[str] = None,
                 contact_id: Optional[int] = None) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = [Phone(phone)] if phone else []
        self.birthday: Birthday = Birthday(birthday) if birthday else ''
        self.address: Address = Address(address) if address else ''
        self.email: Email = Email(email) if email else ''
        self.contact_id = contact_id

        if not self.contact_id:
            self.__save_record()

    def __save_record(self) -> None:
        str_phones = json.dumps([x.value for x in self.phones])

        with self.db_session() as session:
            contact = session.merge(
                models.ModelContacts(
                    name=self.name.value,
                    phones=str_phones,
                    birthday=self.birthday.value,
                    address=self.address.value,
                    email=self.email.value
                )
            )

            try:
                session.commit()
            except exc.IntegrityError as e:

                if str(e.orig) == "UNIQUE constraint failed: notes.note":
                    raise ValueError(f"This contact is already created.")

                print(e)

            self.contact_id = contact.id

    def remove_record(self) -> None:
        with self.db_session() as session:
            session.execute(
                delete(models.ModelContacts)
                .where(models.ModelContacts.id == self.contact_id)
            )
            session.commit()

    def add_phone(self, phone: str) -> Phone:
        phone = Phone(phone)

        if any((phone.value == x.value) for x in self.phones):
            raise ValueError(f"Number '{phone.value}' was already added earlier")

        self.phones.append(phone)

        self.__update_contact_db(
            update(models.ModelContacts)
            .where(models.ModelContacts.id == self.contact_id)
            .values(phones=json.dumps([x.value for x in self.phones]))
        )

        return phone

    def replace_phone(self, index: int, phone: str) -> Phone:
        _phone = self.phones[index - 1]
        _phone.value = phone

        self.__update_contact_db(
            update(models.ModelContacts)
            .where(models.ModelContacts.id == self.contact_id)
            .values(phones=json.dumps([x.value for x in self.phones]))
        )

        return _phone

    def remove_phone(self, index: int) -> Phone:
        phone = self.phones.pop(index - 1)

        self.__update_contact_db(
            update(models.ModelContacts)
            .where(models.ModelContacts.id == self.contact_id)
            .values(phones=json.dumps([x.value for x in self.phones]))
        )

        return phone

    def change_birthday(self, value: str) -> Birthday:
        self.birthday = Birthday(value)

        self.__update_contact_db(
            update(models.ModelContacts)
            .where(models.ModelContacts.id == self.contact_id)
            .values(birthday=self.birthday.value)
        )

        return self.birthday

    def days_to_birthday(self) -> Optional[int]:
        if not self.birthday:
            return

        birthday = self.birthday.value
        today = date.today()

        if self.birthday.value.replace(year=today.year) >= today:
            birthday = birthday.replace(year=today.year)

        else:
            birthday = birthday.replace(year=today.year + 1)

        return (birthday - today).days

    def change_email(self, value: str) -> Email:
        self.email = Email(value)

        self.__update_contact_db(
            update(models.ModelContacts)
            .where(models.ModelContacts.id == self.contact_id)
            .values(email=self.email.value)
        )
        
        return self.email

    def change_address(self, value: str) -> Address:
        self.address = Address(value)

        self.__update_contact_db(
            update(models.ModelContacts)
            .where(models.ModelContacts.id == self.contact_id)
            .values(address=self.address.value)
        )

        return self.address

    def format_record(self) -> str:
        phones = ', '.join([str(x.value) for x in self.phones])
        birthday = self.birthday.value if self.birthday else '–'
        address = self.address.value if self.address else '–'
        email = self.email.value if self.email else '–'

        return f": {self.name.value:^15} : {email:^15} : {str(birthday):^10} : {phones:^30} : {address:^30} :\n"

    def __update_contact_db(self, request: str):
        with self.db_session() as session:
            session.execute(request)
            session.commit()

    def __repr__(self):
        return "Record({})".format(', '.join([f"{k}={v}" for k, v in self.__dict__.items()]))
