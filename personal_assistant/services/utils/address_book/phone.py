from re import search

from personal_assistant.services.utils.field import Field


CODES_MOBILE_UA = ['067', '096', '097', '098',
                   '050', '066', '095', '099',
                   '063', '073', '093',
                   '070', '080', '090', '056', '057',
                   '091', '092', '094']


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        self._value: int = self.__check_phone_number(value)

    @staticmethod
    def __check_phone_number(phone: str) -> int:
        clean_phone = (
                        phone.strip()
                        .removeprefix("+")
                        .replace("(", "")
                        .replace(")", "")
                        .replace("-", "")
                        .replace(" ", "")
                    )

        codes = '|'.join(CODES_MOBILE_UA)

        pattern = r"(?:38|8)?(?:" + codes + r")\d{7}"

        phone = search(pattern, clean_phone)

        if not phone:
            raise ValueError(f"Phone number {clean_phone} is not valid")

        phone = phone.group()

        if phone.startswith('8'):
            return int('3' + phone)
        elif phone.startswith('0'):
            return int('38' + phone)

        return int(phone)
