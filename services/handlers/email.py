from services.decorators import input_error, route
from services.utils import AddressBook


@route("change-email")
@input_error
def change_contact_email(name: str) -> str:
    """
    По этой команде изменяет email для существующего контакта.
    Пользователь вводит команду change-email и имя, обязательно через пробел.
    Пример команды: change-email UserName
    """
    contact = AddressBook()[name]

    email = input(
        f"Enter the email of the contact '{name}' in the format example@domain.com: ")

    contact.change_email(email)

    return f"\nEmail {contact.email.value} of the contact '{name}' successfully saved"
