from functools import wraps

from colorama import Fore


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs) -> None:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(Fore.RED + f"{e}\n")
        except KeyError as e:
            print(Fore.RED + f"User {e} not found\n")
        except IndexError as e:
            print(Fore.RED + f"{e}\n")

    return inner
