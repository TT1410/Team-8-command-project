from typing import Optional
from datetime import date

from .name import Name
from .phone import Phone
from .birthday import Birthday
from .address import Address
from .email import Email


class Record:
    def __init__(self,
                 name: str,
                 phone: Optional[str] = None,
                 birthday: Optional[str] = None,
                 address: Optional[str] = None,
                 email: Optional[str] = None) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = [Phone(phone)] if phone else []
        self.birthday: Birthday = Birthday(birthday) if birthday else ''
        self.address: Address = Address(address) if address else ''
        self.email: Email = Email(email) if email else ''

    def add_phone(self, phone: str) -> Phone:
        phone = Phone(phone)

        if any((phone.value == x.value) for x in self.phones):
            raise ValueError(f"Number '{phone.value}' was already added earlier")

        self.phones.append(phone)

        return phone

    def replace_phone(self, index: int, phone: str) -> tuple[Phone, Phone]:
        old_phone = self.phones.pop(index - 1)
        new_phone = self.add_phone(phone)

        return old_phone, new_phone

    def change_birthday(self, value: str) -> Birthday:
        self.birthday = Birthday(value)

        return self.birthday

    def remove_phone(self, index: int) -> Phone:
        return self.phones.pop(index - 1)

    def days_to_birthday(self) -> Optional[int]:
        if not self.birthday:
            return

        birthday = self.birthday.value
        today = date.today()

        if (birthday.month >= today.month) and (birthday.day >= today.day):
            birthday = birthday.replace(year=today.year)

        elif birthday.month <= today.month:
            birthday = birthday.replace(year=today.year + 1)

        return (birthday - today).days

    def __repr__(self):
        return "Record({})".format(', '.join([f"{k}={v}" for k, v in self.__dict__.items()]))
