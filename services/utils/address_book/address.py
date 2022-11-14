from re import search

from services.utils.field import Field


class Address(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.value: str = value

    @Field.value.setter
    def value(self, value):
        self._value: str = self.check_name(value)

    @classmethod
    def check_name(cls, value: str) -> str:
        clean_value = value.strip()
        pattern = r'(?!^\d+$)^.+$'

        if not search(pattern, clean_value) or len(clean_value) < 3 or len(clean_value) > 30:
            raise ValueError(f"Address '{clean_value}' is not valid")

        return clean_value
