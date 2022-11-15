from typing import Optional

from services.decorators import input_error, route
from services.utils import AddressBook


@route('add-phone')
@input_error
def add_phone_to_contact(name: str) -> str:
    """
    With this command, the bot saves a new phone number for an existing contact in memory.
    The user enters the "add-phone" command and the name, necessarily separated by a space.
    Command example: add-phone UserName
    """
    contact = AddressBook()[name]

    phone = contact.add_phone(input("Enter phone number: "))

    return f"Contact phone number {name} '{phone.value}' successfully added"


@route("change-phone")
@input_error
def change_contact_phone(name: str) -> Optional[str]:
    """
    On this command, the bot replaces the old phone number with the new one for the existing contact.
    The user enters the "change-phone" command and the name, necessarily separated by a space.
    Next, the user will be prompted to select from the list the number that needs to be replaced with a new one.
    Command example: change-phone UserName
    """
    contact = AddressBook()[name]

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
            new_phone = contact.replace_phone(index, new_phone)
        except IndexError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
        else:
            break

    return f"Contact {name} phone number has been successfully replaced to '{new_phone.value}'"


@route("remove-phone")
@input_error
def remove_contact_phone(name: str) -> Optional[str]:
    """
    With this command, the bot deletes the phone number of an existing contact.
    The user enters the "remove-phone" command and the name, necessarily separated by a space.
    Next, you will be prompted to select the number from the list that you want to delete.
    Command example: remove-phone UserName
    """
    contact = AddressBook()[name]

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
            phone = contact.remove_phone(index)
        except IndexError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
        else:
            break

    return f"\nContact phone number {name} '{phone.value}' deleted successfully"


@route("phone")
@input_error
def contact_phones(name: str) -> str:
    """
    By this command, the bot displays the phone numbers for the specified contact in the console.
    The user enters the "phone" command and the name of the contact whose numbers need to be shown, separated by a space.
    Command example: phone UserName
    """
    contact = AddressBook()[name]

    return (f"Phone numbers of {name}\n\t" +
            "\n\t".join([f"{num}. {x.value}" for num, x in enumerate(contact.phones, 1)]))
