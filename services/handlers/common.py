from pathlib import Path
from time import sleep

from colorama import Fore

from services.decorators import input_error, route
from services.utils import ROUTE_MAP
from services.utils.sort_files import DIR_SUFF_DICT, FOUND_FILES, sort


@route("hello")
def hello() -> str:
    """
    Responds to the console "How can I help you?"
    """
    return "How can I help you?"


@route("help")
def help_command() -> str:
    """
    Displays a list of available commands.
    """
    report_commands = ""

    for commands, func in ROUTE_MAP.items():
        report_commands += Fore.CYAN + str(commands) + Fore.YELLOW + (func.__doc__ or '\n\t- - -') + '\n'

    return report_commands


@route(["good-bye", "close", "exit"])
def close_bot() -> str:
    """
    For any of the commands, the bot completes its work.
    """
    return "Good bye!"


@route("echo")
def print_name(value: str = None) -> str:
    """
    Returns the entered text.
    """
    return value


@route("sort-files")
@input_error
def sorting_files_in_a_dir(path: str) -> str:
    """
    The "sort-files" command sorts the files and folders in the target directory. 
    In the course of work, the file extension is checked and, depending on the extension, 
    a decision is made to which category this file belongs.
    The command takes one argument - this is the name of the folder in which it will sort.
    Command example: sort-files /user/Desktop/other
    """
    root_folder = Path(path)

    if not root_folder.exists():
        raise ValueError("[-] Nonexistent directory")

    elif root_folder.is_file():
        raise ValueError("[-] The file is located at this path")

    while True:
        text = input(
            f"{Fore.CYAN}Confirm the sorting of the files in the directory "
            f"{Fore.MAGENTA}'{root_folder.absolute()}' {Fore.CYAN}(yes/no):{Fore.RESET} ")

        if text.lower() == "yes":
            break
        elif text.lower() == "no":
            return "File sorting canceled"

    extensions = []

    for ext in DIR_SUFF_DICT.values():
        extensions.extend(ext)

    print(f"{Fore.YELLOW}Search for files with the following extensions: {Fore.CYAN}{extensions}")
    sleep(5)

    sort(root_folder)

    return ("""\n[!] Sorting is complete
    Found {cyan}{images_len}{yellow} files of category images: {cyan}{images}{yellow}
    Found {cyan}{documents_len}{yellow} files of category documents: {cyan}{documents}{yellow}
    Found {cyan}{audio_len}{yellow} files of category audio: {cyan}{audio}{yellow}
    Found {cyan}{video_len}{yellow} files of category video: {cyan}{video}{yellow}
    Found and unpacked {cyan}{archives_len}{yellow} files of category archives: {cyan}{archives}{yellow}
    Found {cyan}{unknown_len}{yellow} files with unknown extension: {cyan}{unknown}
    """.format(
        cyan=Fore.CYAN,
        yellow=Fore.YELLOW,
        images_len=len(FOUND_FILES['images']),
        documents_len=len(FOUND_FILES['documents']),
        audio_len=len(FOUND_FILES['audio']),
        video_len=len(FOUND_FILES['video']),
        archives_len=len(FOUND_FILES['archives']),
        unknown_len=len(FOUND_FILES['unknown']),
        **FOUND_FILES
    ))
