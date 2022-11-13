from datetime import date, timedelta
from typing import Optional

from services.decorators import input_error, route
from services.utils import ADDRESS_BOOK


@route("change-bd")
@input_error
def change_contact_birthday(name: str) -> str:
    """
    По этой команде изменяет день рождения для существующего контакта.
    Пользователь вводит команду change-bd и имя обязательно через пробел.
    Пример команды: change-bd UserName
    """
    contact = ADDRESS_BOOK()[name]

    birthday = input(
        f"Enter the date of birth of the contact '{name}' in the format YYYY.MM.DD or DD.MM.YYYY: ")

    contact.change_birthday(birthday)

    # Temporary command due to impossibility to change object in the file
    ADDRESS_BOOK().change_contact(contact)

    return f"\nDate of birth {contact.birthday.value} of the contact '{name}' successfully saved"


@route("search-bd")
@input_error
def search_birthday_boy(days: str) -> Optional[str]:
    """
    По этой команде бат выводит в консоль все контакты, у которых день рождения через заданное количество дней.
    Пользователь вводит команду search-birthday и количество дней, обязательно через пробел.
    Пример команды: search-bd 520
    """
    try:
        days = int(days)
    except ValueError:
        raise ValueError("Можно вводить только целые числа.")

    format_contacts = ""
    target_date = date.today() + timedelta(days=days)

    for contact in ADDRESS_BOOK().get_all_contacts():
        if not contact.birthday:
            continue

        birthday = contact.birthday.value

        if target_date.month == birthday.month and target_date.day == birthday.day:
            phones = ', '.join([str(x.value) for x in contact.phones])
            birthday = contact.birthday.value if contact.birthday else '–'
            address = contact.address.value if contact.address else '–'
            email = contact.email.value if contact.email else '–'

            format_contacts += f"{contact.name.value:<10} : {address:^15} : {email:^10} : {birthday:^10} : {phones:^12}\n"

    return (f"{'Name':<10} : {'Address':^15} : {'Email':^10} : {'Birthday':^10} : {'Phones':^12}\n" +
            format_contacts) if format_contacts else "Нет ни одного именинника в этот день"


@route("days-bd")
@input_error
def days_before_birthday(name: str) -> str:
    """
    По этой команде бот выводит в консоль, сколько осталось дней до дня рождения контакта.
    Пользователь вводит команду days-bd и имя контакта, обязательно через пробел.
    Пример команды: days-bd UserName
    """
    days = ADDRESS_BOOK()[name].days_to_birthday()

    return (f"Until the birthday of {name} {days} days" if days else
            f"Contact '{name}' does not have a birthday recorded. "
            f"To add or change a contact's birthday, use the <change-bd>")
