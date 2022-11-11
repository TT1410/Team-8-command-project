import inspect
from types import FunctionType

from services.decorators import input_error
from .register_handlers import ROUTE_MAP


@input_error
def text_parsing(data: str) -> tuple[FunctionType, list[str] | None]:
    command, *args = data.strip().split(' ', maxsplit=1)

    for _command, func in ROUTE_MAP.items():

        if (isinstance(_command, tuple) and command.lower() in _command) or command.lower() == _command:

            if check_args(func, args):
                return func, args

            return func, None
    else:
        raise ValueError("You entered an unknown command. Please enter the required command.\n")


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
                         f"\nArguments command: <{all_args}>")

    required_args = ' '.join(func_args[:len(func_args_defaults)] if
                             func_args_defaults else func_args)

    raise ValueError(f"Not all mandatory command arguments are listed: <{required_args}>\n")
