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
        raise ValueError("[-] Nonexistent directory")

    elif root_folder.is_file():
        raise ValueError("[-] The file is located at this path")

    while True:
        text = input(
            f"Confirm the sorting of the files in the directory '{root_folder.absolute()}' (yes/no): ")

        if text.lower() == "yes":
            break
        elif text.lower() == "no":
            return "File sorting canceled"

    extensions = []

    for ext in DIR_SUFF_DICT.values():
        extensions.extend(ext)

    print(f"Search for files with the following extensions: {extensions}")
    sleep(5)

    sort(root_folder)

    return ("""\n[!] Sorting is complete
    Found {images_len} files of category images: {images}
    Found {documents_len} files of category documents: {documents}
    Found {audio_len} files of category audio: {audio}
    Found {video_len} files of category video: {video}
    Found and unpacked {archives_len} files of category archives: {archives}
    Found {unknown_len} files with unknown extension: {unknown}
    """.format(
        images_len=len(FOUND_FILES['images']),
        documents_len=len(FOUND_FILES['documents']),
        audio_len=len(FOUND_FILES['audio']),
        video_len=len(FOUND_FILES['video']),
        archives_len=len(FOUND_FILES['archives']),
        unknown_len=len(FOUND_FILES['unknown']),
        **FOUND_FILES
    ))
