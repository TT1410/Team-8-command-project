from services.decorators import input_error, route
from services.utils import notes


@route('add-note')
@input_error
def add_note(text: str) -> str:
    """
    По этой команде бот сохраняет в памяти новая заметка.
    Пользователь вводит команду add-note и текст, обязательно через пробел.
    Пример команды: add-note lorem ipsum dolor sit amet
    """
    note = notes.Record(text)

    tag_input = input("Enter text separated by space: ")

    if tag_input:
        tags = tag_input.split(" ")
        note.add_tags(tags)

    return "Note was successfully added"
