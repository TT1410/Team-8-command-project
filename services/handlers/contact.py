from typing import Optional

from services.decorators import input_error, route
from services.utils import AddressBook, Record


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

    if AddressBook().get_contact(name):
        raise ValueError(f"Contact with the name {name} already exists. "
                         f"To add a new number to an existing contact, use the <change-contact> command.")

    AddressBook().add_record(Record(**locals()))

    return f"Successfully created a new contact '{name}'"


@route("remove-contact")
@input_error
def remove_contact(name: str) -> str:
    """
    По этой команде бот удаляет контакт.
    Пользователь вводит команду remove-contact и имя, обязательно через пробел.
    Пример команды: remove-contact UserName
    """
    contact = AddressBook()[name]

    # Temporary command due to impossibility to change object in the file
    AddressBook().change_contact(contact, remove=True)

    return f"Successfully deleted contact '{name}'"


@route("show-all")
@input_error
def show_all_users() -> str:
    """
    По этой команде бот выводит все сохраненные контакты со всеми данными в консоль.
    """
    format_contacts = ""

    for contacts in AddressBook().iterator(1):
        contact = contacts[0]

        format_contacts += contact.format_record()

    return (f": {'Name':^15} : {'Email':^15} : {'Birthday':^10} : {'Phones':^30} : {'Address':^30} :\n" +
            format_contacts) if format_contacts else "Не сохранено ни одного контакта."


@route("search-contacts")
def search_contacts(search_value: str) -> Optional[str]:
    """
    По этой команде бот выводит в консоль всех контактов, у которых есть совпадение со строкой поиска в имени, или номере.
    Пользователь вводит команду search-contacts и имя контакта, обязательно через пробел.
    Пример команды: search-contact any
    """
    contacts = AddressBook().search_contacts(search_value)

    if not contacts:
        return "Не найдено ни одного контакта."

    format_contacts = ""

    for contact in contacts:
        format_contacts += contact.format_record()

    return (f": {'Name':^15} : {'Email':^15} : {'Birthday':^10} : {'Phones':^30} : {'Address':^30} :\n" +
            format_contacts)
