from services.decorators import input_error, route
from services.utils import AddressBook


@route("change-address")
@input_error
def change_contact_address(name: str) -> str:
    """
    По этой команде изменяет адрес для существующего контакта.
    Пользователь вводит команду change-adress и имя, обязательно через пробел.
    Пример команды: change-address UserName
    """
    contact = AddressBook()[name]

    address = input(f"Enter the address of the contact '{name}': ")

    contact.change_address(address)

    return f"\nAddress '{contact.address.value}' of the contact '{name}' successfully saved"
