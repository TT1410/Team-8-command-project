from re import search

from .field import Field


class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.value: str = value

    @Field.value.setter
    def value(self, value):
        self._value: str = self.check_name(value)

    @staticmethod
    def check_name(value: str) -> str:
        clean_value = (
            value.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .capitalize()
        )

        if search(r"\d+", clean_value) or len(clean_value) < 3 or len(clean_value) > 30:
            raise ValueError(f"Name '{clean_value}' is not valid")

        return clean_value
