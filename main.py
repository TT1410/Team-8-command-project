from termcolor import colored
from colorama import init

from services.db import create_all_tables
from services.utils import text_parsing

init()


def main() -> None:
    create_all_tables()

    print(
        colored(
      '''\nDeveloped by GoIt Team 8
         \nYour personal assistant welcomes you.
         \nType "help" to see the commands
        ''', "green"
        )
    )

    while True:
        text = input("\nEnter command: ")

        result = text_parsing(text)

        if not result:
            continue

        func, args = result

        result = func(*args) if args else func()

        if result:
            print(f"{result}")

        if result == "Good bye!":
            break


if __name__ == '__main__':
    main()
