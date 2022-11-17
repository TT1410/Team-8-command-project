from colorama import init, Fore

from .services.db import create_all_tables
from .services.utils import text_parsing

init(autoreset=True)


def main() -> None:
    create_all_tables()

    print(f"{Fore.GREEN}"
          f"Developed by GoIt Team 8\n\n"
          f"Your personal assistant welcomes you.\n\n"
          f"Type {Fore.MAGENTA}«help»{Fore.GREEN} to see all available commands"
          )

    while True:
        text = input("\nEnter command: ")

        result = text_parsing(text)

        if not result:
            continue

        func, args = result

        result = func(*args) if args else func()

        if result:
            print(Fore.YELLOW + f"{result}")

        if result == "Good bye!":
            break


if __name__ == '__main__':
    main()
