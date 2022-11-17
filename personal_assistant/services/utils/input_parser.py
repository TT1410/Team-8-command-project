import inspect
from types import FunctionType

from colorama import Fore

from personal_assistant.services.decorators import input_error
from .register_handlers import ROUTE_MAP
from .selection_of_teams import selection_of_teams


@input_error
def text_parsing(data: str) -> tuple[FunctionType, list[str] | None]:
    command, *args = data.strip().split(' ', maxsplit=1)

    for _command, func in ROUTE_MAP.items():

        if (isinstance(_command, tuple) and command.lower() in _command) or command.lower() == _command:

            if check_args(func, args):
                return func, args

            return func, None
    else:
        if not command:
            raise ValueError(f"To view a list of available commands with descriptions, type {Fore.MAGENTA}«help»\n")

        suggest_commands = selection_of_teams(command)

        if not suggest_commands:
            raise ValueError(f"You entered an unknown command {Fore.MAGENTA}«{command}»{Fore.RED}. "
                             f"Please enter the required command.\n"
                             f"To view a list of available commands with descriptions, type {Fore.MAGENTA}«help»\n")

        raise ValueError(f"Perhaps you wanted to enter one of the {Fore.MAGENTA}{suggest_commands}{Fore.RED} commands?")


def check_args(func, args: list) -> bool:
    func_params = inspect.getfullargspec(func.__dict__.get('__wrapped__', func))

    func_args = func_params.args
    func_args_defaults = func_params.defaults or []

    if not func_args:
        return False

    if len(func_args) == len(args) and args[0]:
        return True

    elif len(args) >= (len(func_args)-len(func_args_defaults)) <= len(args):
        return True

    elif len(args) > len(func_args):
        all_args = ' '.join(func_args)
        raise ValueError(f"More arguments are listed than the command can accept. "
                         f"\nArguments command: {Fore.MAGENTA}«{all_args}»")

    required_args = ' '.join(func_args[:len(func_args_defaults)] if
                             func_args_defaults else func_args)

    raise ValueError(f"Not all mandatory command arguments are listed: {Fore.MAGENTA}«{required_args}»\n")
