from services.decorators import input_error, route
from services.utils import notes, Notes


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


@route('search-tags')
@input_error
def search_notes_by_tags(tags: str) -> str:
    """
    По этой команде бот ищет в памяти заметку по тегам.
    Пользователь вводит через пробел команду search-tags и тег/теги через пробел по которым будет происходить поиск.
    Пример команды: search-tags tag1 tag2
    """

    tags = tags.split()
    tags.sort()

    results: dict[str, list[notes.Record]] = {tag: notes.Notes().search_notes_by_tags([tag]) for tag in tags}

    if not results:
        return "Note was not found."

    format_results = ""

    for key, value in results.items():
        note = '\n\tNote: '.join([str(x.text.value) for x in value])
        format_results += f"{key}\n\tNote: {note}\n"

    return format_results


def find_note_by_index() -> notes.Record | str:
    dict_indexes = {}

    num = 1

    for note in Notes().get_all_records():
        dict_indexes[num] = note._id

        print(f"{num}. \t{note.format_record()}")

        num += 1

    if num == 1:
        return "No notes"

    while True:
        try:
            index = int(
                input("Enter the index of the note from the list: "))
        except ValueError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
            continue

        if index == 0:
            return "Cancel"

        try:
            return Notes().search_notes_by_id(dict_indexes[index])
        except KeyError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")


@route('add-tags')
def add_tags_to_notes() -> str:
    """
    По этой команде бот добавляет теги для существующей записи.
    Пользователь вводит команду add-tags.
    Далее пользователю будет предложено ввести теги, разделенные пробелом.
    Пример команды: add-tags
    """
    note = find_note_by_index()

    if isinstance(note, str):
        return note

    tag_input = None

    while not tag_input:
        tag_input = input("Enter tags separated by space: ")

    note.add_tags(tag_input.split(" "))

    return 'The tags have been added successfully'


@route('change-note')
def change_note() -> str:
    """
    По этой команде бот изменяет ранее сохраненные заметки.
    Пользователь вводит команду change-note.
    Далее пользователю будет предложено ввести новый текст заметки.
    Пример команды: change-note
    """
    note = find_note_by_index()

    if isinstance(note, str):
        return note

    new_text = None

    while not new_text:
        new_text = input("Enter new note: ")

    note.replace_text(new_text)

    return 'Note was successfully change'


@route('delete-note')
def delete_note() -> str:
    """
    По этой команде бот удаляет ранее сохраненнуе заметку.
    Пользователь вводит команду delete-note.
    Далее пользователю будет предложено выбрать из списка заметку для удаления.
    Пример команды: delete-note
    """
    note = find_note_by_index()

    if isinstance(note, str):
        return note

    note.remove_record()
    
    return 'Note was successfully deleted'
