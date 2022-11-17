from typing import Optional

from personal_assistant.services.decorators import input_error, route
from personal_assistant.services.utils import AddressBook, address_book


@route("add-contact")
@input_error
def add_contact(name: str) -> str:
    """
    On this command, the bot saves a new contact in memory.
    The user enters the "add-contact" command and the name, necessarily separated by a space.
    Command example: add-contact UserName
    """
    address_book.Name(name)

    phone = input("Enter phone number: ")
    address_book.Phone(phone) if phone else None

    birthday = input("Enter date of birth (YYYY.MM.DD or DD.MM.YYYY): ")
    address_book.Birthday(birthday) if birthday else None

    address = input("Enter address: ")
    address_book.Address(address) if address else None

    email = input("Enter email (example@domain.com): ")
    address_book.Email(email) if email else None

    contact = address_book.Record(**locals())

    return f"Successfully created a new contact '{contact.name.value}'"


@route("remove-contact")
@input_error
def remove_contact(name: str) -> str:
    """
    On this command, the bot deletes the contact.
    The user enters the "remove-contact" command and the name, necessarily separated by a space.
    Command example: remove-contact UserName
    """
    contact = AddressBook()[name]

    contact.remove_record()

    return f"Successfully deleted contact '{name}'"


@route("show-all")
@input_error
def show_all_users() -> str:
    """
    By this command, the bot displays all saved contacts with all the data to the console.
    """
    format_contacts = ""

    for contacts in AddressBook().iterator(1):
        contact = contacts[0]

        format_contacts += contact.format_record()

    return (f": {'Name':^15} : {'Email':^15} : {'Birthday':^10} : {'Phones':^30} : {'Address':^30} :\n" +
            format_contacts) if format_contacts else "No contact has been saved."


@route("search-contacts")
def search_contacts(search_value: str) -> Optional[str]:
    """
    By this command, the bot displays in the console all contacts that have a match with the search string in the name or number.
    The user enters the "search-contacts" command and the name of the contact, separated by a space.
    Command example: search-contact any
    """
    contacts = AddressBook().search_contacts(search_value)

    if not contacts:
        return "No contact found."

    format_contacts = ""

    for contact in contacts:
        format_contacts += contact.format_record()

    return (f": {'Name':^15} : {'Email':^15} : {'Birthday':^10} : {'Phones':^30} : {'Address':^30} :\n" +
            format_contacts)
