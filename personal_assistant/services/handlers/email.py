from personal_assistant.services.decorators import input_error, route
from personal_assistant.services.utils import AddressBook


@route("change-email")
@input_error
def change_contact_email(name: str) -> str:
    """
    This command changes the email for an existing contact.
    The user enters the "change-email" command and a name, necessarily separated by a space.
    Command example: change-email UserName
    """
    contact = AddressBook()[name]

    email = input(
        f"Enter the email of the contact '{name}' in the format example@domain.com: ")

    contact.change_email(email)

    return f"\nEmail {contact.email.value} of the contact '{name}' successfully saved"
