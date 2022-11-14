from .register_handlers import ROUTE_MAP


def selection_of_teams(command: str) -> list[str]:
    def command_filter(cmd: str | tuple) -> bool:
        if isinstance(cmd, tuple):
            return any(command in x for x in cmd)

        return command in cmd

    def get_one_command(cmd: str | tuple) -> str:
        if isinstance(cmd, tuple):
            cmd = next(filter(lambda x: command in x, cmd))

        return cmd

    suggest_commands = [get_one_command(y) for y in [x for x in filter(command_filter, ROUTE_MAP.keys())]]

    suggest_commands.sort(key=lambda x: x.find(command))

    return suggest_commands
