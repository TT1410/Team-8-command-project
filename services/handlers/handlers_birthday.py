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
