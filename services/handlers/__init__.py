# from console_bot.services.utils import register_message_handler
from .handlers_address import change_contact_address
from .handlers_birthday import change_contact_birthday, days_before_birthday
from .handlers_common import (
    hello, help_command, close_bot, print_name
)
from .handlers_contact import (
    add_contact, remove_contact, show_all_users, search_contacts
)
from .handlers_email import change_contact_email
from .handlers_phone import (
    add_phone_to_contact, change_contact_phone, remove_contact_phone, contact_phones
)

# register_message_handler(hello, 'hello')
# register_message_handler(add_user, 'add', 3)
# register_message_handler(add_phone, 'add-phone', 2)
# register_message_handler(change_phone, 'change-phone', 2)
# register_message_handler(remove_phone, 'remove-phone', 1)
# register_message_handler(user_phone, 'phone', 1)
# register_message_handler(show_all_users, 'show all')
# register_message_handler(close_bot, ["good bye", "close", "exit"])
# register_message_handler(help_command, "help")
