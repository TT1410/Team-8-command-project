from services.db import create_all_tables
from services.utils import text_parsing


def main() -> None:
    create_all_tables()

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
