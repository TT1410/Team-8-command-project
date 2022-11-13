from services.decorators import route
from services.utils import ROUTE_MAP


@route("hello")
def hello() -> str:
    """
    Отвечает в консоль "How can I help you?"
    """
    return "How can I help you?"


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
