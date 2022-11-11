from re import search

from .field import Field


class Email(Field):

    def __init__(self, value: str):
        super().__init__(value)
        self.value: str = value

    @Field.value.setter
    def value(self, value):
        self._value: str = self.__check_email(value)

    @staticmethod
    def __check_email(email: str) -> str:
        clean_email = (
                        email.strip()
                        .removeprefix("+")
                        .replace("(", "")
                        .replace(")", "")
                        .replace("-", "")
                        .replace(" ", "")
                    )

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        email = search(pattern, clean_email)

        if not email:
            raise ValueError(f"Email {clean_email} is not valid")

        email = email.group()

        return email