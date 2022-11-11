from services.utils import text_parsing


def main() -> None:
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
