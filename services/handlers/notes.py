from services.decorators import input_error, route
from services.utils import notes


@route('add-note')
@input_error
def add_note(text: str) -> str:
    """
    По этой команде бот сохраняет в памяти новую заметку.
    Пользователь вводит команду add-note и текст, обязательно через пробел.
    Пример команды: add-note lorem ipsum dolor sit amet
    """
    note = notes.Record(text)

    tag_input = input("Enter tags separated by space: ")

    if tag_input:
        tags = tag_input.split(" ")
        note.add_tags(tags)

    return "Note was successfully added"


@route('search-text')
@input_error
def search_notes_by_text(text: str) -> str:
    """
    По этой команде бот ищет в памяти заметку по тексту.
    Пользователь вводит через пробел команду search-text и текст по которому будет происходить поиск.
    Пример команды: search-text lorem ipsum dolor sit amet
    """
    results = notes.Notes().search_notes_by_text(text)

    if not results:
        return "Note was not found."

    format_results = ""

    for result in results:
        format_results += result.format_record() + '\n'

    return format_results
