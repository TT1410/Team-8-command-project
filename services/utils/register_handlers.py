from types import FunctionType


ROUTE_MAP = {}


def register_message_handler(func: FunctionType, commands: str | list) -> FunctionType:
    if isinstance(commands, list):
        commands = tuple(commands)

    ROUTE_MAP[commands] = func

    return func
