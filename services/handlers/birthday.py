from datetime import date, timedelta
from typing import Optional

from services.decorators import input_error, route
from services.utils import AddressBook


@route("change-bd")
@input_error
def change_contact_birthday(name: str) -> str:
    """
    This command changes the birthday for an existing contact.
    The user enters the "change-bd" command and the name, must be separated by a space.
    Command example: change-bd UserName
    """
    contact = AddressBook()[name]

    birthday = input(
        f"Enter the date of birth of the contact '{name}' in the format YYYY.MM.DD or DD.MM.YYYY: ")

    contact.change_birthday(birthday)

    return f"\nDate of birth {contact.birthday.value} of the contact '{name}' successfully saved"


@route("search-bd")
@input_error
def search_birthday_boy(days: str) -> Optional[str]:
    """
    By this command, the bat displays in the console all contacts who have a birthday in a given number of days.
    The user enters the "search-birthday" command followed by the number of days, separated by a space.
    Command example: search-bd 520
    """
    try:
        days = int(days)
    except ValueError:
        raise ValueError("Only whole numbers can be entered.")

    format_contacts = ""
    target_date = date.today() + timedelta(days=days)

    for contact in AddressBook().get_all_contacts():
        if not contact.birthday:
            continue

        birthday = contact.birthday.value

        if target_date.month == birthday.month and target_date.day == birthday.day:
            format_contacts += contact.format_record()

    return (f": {'Name':^15} : {'Email':^15} : {'Birthday':^10} : {'Phones':^30} : {'Address':^30} :\n" +
            format_contacts) if format_contacts else "There is no birthday on this day"


@route("days-bd")
@input_error
def days_before_birthday(name: str) -> str:
    """
    By this command, the bot displays in the console how many days are left until the contact's birthday.
    The user enters the "days-bd command" followed by the contact name, separated by a space.
    Command example: days-bd UserName
    """
    days = AddressBook()[name].days_to_birthday()

    return (f"Until the birthday of {name} {days} days" if days else
            f"Contact '{name}' does not have a birthday recorded. "
            f"To add or change a contact's birthday, use the <change-bd>")
