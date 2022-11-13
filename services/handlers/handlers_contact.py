from typing import Optional

from services.decorators import input_error, route
from services.utils import ADDRESS_BOOK, Record


@route("add-contact")
@input_error
def add_contact(name: str) -> str:
    """
    По этой команде бот сохраняет в памяти новый контакт.
    Пользователь вводит команду add-contact и имя, обязательно через пробел.
    Пример команды: add-contact UserName
    """
    phone = input("Enter phone number: ")

    birthday = input("Enter date of birth (YYYY.MM.DD or DD.MM.YYYY): ")

    address = input("Enter address: ")

    email = input("Enter email (example@damain.com): ")

    if ADDRESS_BOOK().get_contact(name):
        raise ValueError(f"Contact with the name {name} already exists. "
                         f"To add a new number to an existing contact, use the <change-contact> command.")

    ADDRESS_BOOK().add_record(Record(**locals()))

    return f"Successfully created a new contact '{name}'"


@route("remove-contact")
@input_error
def remove_contact(name: str) -> str:
    """
    По этой команде бот удаляет контакт.
    Пользователь вводит команду remove-contact и имя, обязательно через пробел.
    Пример команды: remove-contact UserName
    """
    contact = ADDRESS_BOOK()[name]

    # Temporary command due to impossibility to change object in the file
    ADDRESS_BOOK().change_contact(contact, remove=True)

    return f"Successfully deleted contact '{name}'"


@route("show-all")
@input_error
def show_all_users() -> str:
    """
    По этой команде бот выводит все сохраненные контакты со всеми данными в консоль.
    """
    format_contacts = f"{'Name':<10} : {'Address':^15} : {'Email':^10} : {'Birthday':^10} : {'Phones':^12}\n"

    for contacts in ADDRESS_BOOK().iterator(1):
        contact = contacts[0]

        phones = ', '.join([str(x.value) for x in contact.phones])
        birthday = contact.birthday.value if contact.birthday else '–'
        address = contact.address.value if contact.address else '–'
        email = contact.email.value if contact.email else '–'

        format_contacts += f"{contact.name.value:<10} : {address:^15} : {email:^10} : {birthday:^10} : {phones:^12}\n"

    return format_contacts


@route("search-contacts")
def search_contacts(search_value: str) -> Optional[str]:
    """
    По этой команде бот выводит в консоль всех контактов, у которых есть совпадение со строкой поиска в имени, или номере.
    Пользователь вводит команду search-contacts и имя контакта, обязательно через пробел.
    Пример команды: search-contact any
    """
    contacts = ADDRESS_BOOK().search_contacts(search_value)

    if not contacts:
        return

    format_contacts = f"{'Name':<10} : {'Address':^15} : {'Email':^10} : {'Birthday':^10} : {'Phones':^12}\n"

    for contact in contacts:
        phones = ', '.join([str(x.value) for x in contact.phones])
        birthday = contact.birthday.value if contact.birthday else '–'
        address = contact.address.value if contact.address else '–'
        email = contact.email.value if contact.email else '–'

        format_contacts += f"{contact.name.value:<10} : {address:^15} : {email:^10} : {birthday:^10} : {phones:^12}\n"

    return format_contacts
