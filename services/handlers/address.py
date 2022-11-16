from services.decorators import input_error, route
from services.utils import AddressBook


@route("change-address")
@input_error
def change_contact_address(name: str) -> str:
    """
    This command changes the address for an existing contact.
    The user enters the "change-adress" command and the name, necessarily separated by a space.
    Command example: change-address UserName
    """
    contact = AddressBook()[name]

    address = input(f"Enter the address of the contact '{name}': ")

    contact.change_address(address)

    return f"\nAddress '{contact.address.value}' of the contact '{name}' successfully saved"
