from re import search

from personal_assistant.services.utils.field import Field


class Email(Field):
    @Field.value.setter
    def value(self, value):
        self._value: str = self.__check_email(value)

    @staticmethod
    def __check_email(email: str) -> str:

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        email = search(pattern, email)

        if not email:
            raise ValueError(f"Email {email} is not valid")

        return email.group()
        