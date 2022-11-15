from pathlib import Path
from time import sleep

from services.decorators import input_error, route
from services.utils import ROUTE_MAP
from services.utils.sort_files import DIR_SUFF_DICT, FOUND_FILES, sort


@route("hello")
def hello() -> str:
    """
    Отвечает в консоль "How can I help you?"
    """
    return "How can I help you?"


@route("help")
def help_command() -> str:
    """
    Выводит список доступных команд.
    """
    report_commands = ""

    for commands, func in ROUTE_MAP.items():
        report_commands += str(commands) + (func.__doc__ or '\n\t- - -') + '\n'

    return report_commands


@route(["good-bye", "close", "exit"])
def close_bot() -> str:
    """
    По любой из команд бот завершает свою роботу.
    """
    return "Good bye!"


@route("echo")
def print_name(value: str = None) -> str:
    """
    Возвращает введенный текст.
    """
    return value


@route("sort-files")
@input_error
def sorting_files_in_a_dir(path: str) -> str:
    
    root_folder = Path(path)

    if not root_folder.exists():
        raise ValueError("[-] Неіснуюча директорія")

    elif root_folder.is_file():
        raise ValueError("[-] За даним шляхом знаходиться файл")

    while True:
        text = input(f"Підтвердіть сортування файлів у каталозі '{root_folder.absolute()}' (так/ні): ")

        if text.lower() == "так":
            break
        elif text.lower() == "ні":
            return "Сортування файлів відмінено"

    extensions = []

    for ext in DIR_SUFF_DICT.values():
        extensions.extend(ext)

    print(f"Пошук файлів з наступними розширеннями: {extensions}")
    sleep(5)

    sort(root_folder)

    return ("""\n[!] Сортування завершено
    Знайдено {images_len} файлів категорії images: {images}
    Знайдено {documents_len} файлів категорії documents: {documents}
    Знайдено {audio_len} файлів категорії audio: {audio}
    Знайдено {video_len} файлів категорії video: {video}
    Знайдено та розпаковано {archives_len} файлів категорії archives: {archives}
    Знайдено {unknown_len} файлів з невідомим розширенням: {unknown}
    """.format(
        images_len=len(FOUND_FILES['images']),
        documents_len=len(FOUND_FILES['documents']),
        audio_len=len(FOUND_FILES['audio']),
        video_len=len(FOUND_FILES['video']),
        archives_len=len(FOUND_FILES['archives']),
        unknown_len=len(FOUND_FILES['unknown']),
        **FOUND_FILES
    ))
