from typing import Optional

from services.decorators import input_error, route
from services.utils import ADDRESS_BOOK, Record, ROUTE_MAP


@route("hello")
def hello() -> str:
    """
    Отвечает в консоль "How can I help you?"
    """
    return "How can I help you?"


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


@route('add-phone')
@input_error
def add_phone_to_contact(name: str) -> str:
    """
    По этой команде бот сохраняет в памяти новый номер телефона для существующего контакта.
    Пользователь вводит команду add-phone, имя и новый номер телефона, обязательно через пробел.
    Пример команды: add-phone UserName 0961233032
    """
    contact = ADDRESS_BOOK()[name]

    phone = contact.add_phone(input("Enter phone number: "))

    # Temporary command due to impossibility to change object in the file
    ADDRESS_BOOK().change_contact(contact)

    return f"Contact phone number {name} '{phone.value}' successfully added"


@route("change-phone")
@input_error
def change_contact_phone(name: str) -> Optional[str]:
    """
    По этой команде бот заменяет старый номер телефона новым для существующего контакта.
    Пользователь вводит команду change-phone и имя, обязательно через пробел.
    Далее пользователю будет предложено выбрать из списка номер, который необходимо заменить новым.
    Пример команды: change-phone UserName 0961233789
    """
    contact = ADDRESS_BOOK()[name]

    new_phone = input("Enter a new phone number: ")

    while True:
        print(contact_phones(name))

        try:
            index = int(
                input("Enter the index number of the phone from the list you want to replace: "))
        except ValueError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
            continue

        if index == 0:
            return

        try:
            old_phone, new_phone = contact.replace_phone(index, new_phone)
        except IndexError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
        else:
            break

    # Temporary command due to impossibility to change object in the file
    ADDRESS_BOOK().change_contact(contact)

    return f"Contact phone number {name} '{old_phone.value}' " \
           f"has been successfully replaced by '{new_phone.value}'"


@route("remove-phone")
@input_error
def remove_contact_phone(name: str) -> Optional[str]:
    """
    По этой команде бот удаляет номер телефона существующего контакта.
    Пользователь вводит команду remove-phon и имя, обязательно через пробел.
    Далее будет предложено выбрать номер из списка, который необходимо удалить.
    Пример команды: remove-phone UserName
    """
    contact = ADDRESS_BOOK()[name]

    while True:
        print(contact_phones(name))

        try:
            index = int(
                input("Enter the index number of the phone from the list you want to remove: "))
        except ValueError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
            continue

        if index == 0:
            return

        try:
            old_phone = contact.remove_phone(index)
        except IndexError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
        else:
            break

    # Temporary command due to impossibility to change object in the file
    ADDRESS_BOOK().change_contact(contact)

    return f"\nContact phone number {name} '{old_phone.value}' deleted successfully"


@route("phone")
@input_error
def contact_phones(name: str) -> str:
    """
    По этой команде бот выводит в консоль номера телефонов для указанного контакта.
    Пользователь вводит команду phone и имя контакта, чьи номера нужно показать, обязательно через пробел.
    Пример команды: phone UserName
    """
    contact = ADDRESS_BOOK()[name]

    return (f"Phone numbers of {name}\n\t" +
            "\n\t".join([f"{num}. {x.value}" for num, x in enumerate(contact.phones, 1)]))


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


@route("change-email")
@input_error
def change_contact_email(name: str) -> str:
    """
    По этой команде изменяет email для существующего контакта.
    Пользователь вводит команду change-email и имя, обязательно через пробел.
    Пример команды: change-email UserName
    """
    contact = ADDRESS_BOOK()[name]

    email = input(
        f"Enter the email of the contact '{name}' in the format example@domain.com: ")

    contact.change_email(email)

    # Temporary command due to impossibility to change object in the file
    ADDRESS_BOOK().change_email(contact)

    return f"\nEmail {contact.email.value} of the contact '{name}' successfully saved"


@route("change-address")
@input_error
def change_contact_address(name: str) -> str:
    """
    По этой команде изменяет адрес для существующего контакта.
    Пользователь вводит команду change-adress и имя, обязательно через пробел.
    Пример команды: change-address UserName
    """
    contact = ADDRESS_BOOK()[name]

    address = input(f"Enter the address of the contact '{name}': ")

    contact.change_address(address)

    # Temporary command due to impossibility to change object in the file
    ADDRESS_BOOK().change_address(contact)

    return f"\nAddress {contact.address.value} of the contact '{name}' successfully saved"


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
    Пример команды: search-contact Tar
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


@route("help")
def help_command() -> str:
    """
    Выводит список доступных команд.
    """
    report_commands = ""

    for commands, func in ROUTE_MAP.items():
        report_commands += str(commands) + (func.__doc__ or '\n\t- - -') + '\n'

    return report_commands


@route(["good-bye", "close", "exit"])
def close_bot() -> str:
    """
    По любой из команд бот завершает свою роботу.
    """
    return "Good bye!"


@route("echo")
def print_name(value: str = None) -> str:
    """
    Возвращает введенный текст.
    """
    return value
