from services.utils import register_message_handler


def route(commands: str | list[str]):
    def wrapper(func):
        register_message_handler(func=func, commands=commands)
        return func
    return wrapper
