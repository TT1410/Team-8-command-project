from .common import (
    hello,
    help_command,
    close_bot,
    print_name,
)
from .contact import (
    add_contact,
    remove_contact,
    show_all_users,
    search_contacts,
)
from .phone import (
    add_phone_to_contact,
    change_contact_phone,
    remove_contact_phone,
    contact_phones,
)
from .birthday import (
    change_contact_birthday,
    days_before_birthday,
)
from .address import change_contact_address
from .email import change_contact_email
from .notes import (
    add_note
)

# from console_bot.services.utils import register_message_handler

# register_message_handler(hello, 'hello')
# register_message_handler(add_user, 'add', 3)
# register_message_handler(add_phone, 'add-phone', 2)
# register_message_handler(change_phone, 'change-phone', 2)
# register_message_handler(remove_phone, 'remove-phone', 1)
# register_message_handler(user_phone, 'phone', 1)
# register_message_handler(show_all_users, 'show all')
# register_message_handler(close_bot, ["good bye", "close", "exit"])
# register_message_handler(help_command, "help")
