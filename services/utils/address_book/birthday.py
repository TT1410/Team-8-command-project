from datetime import date

from services.utils.field import Field


class Birthday(Field):

    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.value: date = value

    @Field.value.setter
    def value(self, value) -> None:
        self._value: date = self.check_date(value)

    @staticmethod
    def check_date(value: str) -> date:
        """
        Format string date is YYYY.MM.DD or DD.MM.YYYY
        Instead of a dot, a comma, dash or colon is allowed
        :param value:
        :return:
        """
        value = value.strip()

        for separator in (".", ",", "-", ":", "/"):
            value, *args = value.split(separator)

            if args:
                break

        if not args or len(args) > 2:
            raise ValueError("Invalide date format. Date format should be YYYY.MM.DD or DD.MM.YYYY.")

        if int(value) > 31:
            return date(int(value), int(args[0]), int(args[1]))

        return date(int(args[1]), int(args[0]), int(value))
