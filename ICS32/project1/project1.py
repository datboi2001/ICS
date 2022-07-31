from pathlib import Path
from shutil import copy2
from os import utime


def _print_object(object: str or list) -> None:
    """Print the word ERROR or NOT TEXT."""
    if type(object) == str:
        print(object)
    else:
        for x in object:
            print(x)


def search_directory(path: Path, recursive: bool, file_list: []) -> bool:
    try:
        for x in path.iterdir():
            if x.is_file():
                file_list.append(x)
        file_list.sort()
        for x in path.iterdir():
            if x.is_dir() and recursive:
                file_list += search_directory(x, True, [])
    except PermissionError or IOEError:
        pass
    finally:
        return file_list


def command_d(path: Path) -> list:
    """Find all of the files in a directory."""
    file_list = []
    files = search_directory(path, False, file_list)
    return files


def command_r(path: Path) -> list:
    """Find all of the files in a directory and in its subdirectories"""
    file_list = []
    files = search_directory(path, True, file_list)
    return files


def command_n(result: list, name: str) -> list:
    """Find files that matches the given name from the parameter."""
    filtered_result = []
    for x in result:
        if x.name == name:
            filtered_result.append(x)
    return filtered_result


def command_e(result: list, ext: str) -> list:
    """Find files that contain the given extension from the parameter."""
    if ext[0] != '.':
        ext = '.' + ext
    filtered_result = []
    for x in result:
        if x.suffix == ext:
           filtered_result.append(x)
    return filtered_result


def command_t(result: list, text: str):
    """Open each file and read to see if it contains the given text from the paramter."""
    filtered_result = []
    for x in result:
        try:
            f = x.open()
            for lines in f.readlines():
                if text in lines:
                    filtered_result.append(x)
                    break
        except UnicodeDecodeError:
            pass
        finally:
            f.close()
    return filtered_result


def command_smaller(result: list, size: int) -> list:
    """Find files smaller than the given size."""
    filtered_result = []
    for x in result:
        if x.stat().st_size < size:
            filtered_result.append(x)
    return filtered_result


def command_bigger(result: list, size: int) -> list:
    """Find files bigger than the given size."""
    filtered_result = []
    for x in result:
        if x.stat().st_size > size:
            filtered_result.append(x)
    return filtered_result


def command_f(result: list) -> None:
    """
    Attempt to read and print the first line of a file.
    Print NOT TEXT if the file cannot be read.
    """
    for files in result:
        f = files.open()
        try:
            _print_object(f.readline().strip())
        except UnicodeDecodeError:
            _print_object("NOT TEXT")
        finally:
            f.close()

def command_copy(result: list) -> None:
    """Copy the files in put it in """
    for files in result:
        copy2(str(files), str(files) + ".dup")


def command_time(result: list) -> None:
    """Change the last modified timestamp to the current date time."""
    for files in result:
        utime(files)


def _first_stage() -> list:
    """The skeleton of the first stage of the program."""
    valid = True
    while valid:
        path = input()
        if path.startswith('D ') and Path(path[2:]).exists():
            file_list = command_d(Path(path[2:]))
            valid = False
        elif path.startswith('R ') and Path(path[2:]).exists():
            file_list = command_r(Path(path[2:]))
            valid = False
        else:
            _print_object("ERROR")
    _print_object(file_list)
    return file_list


def _second_stage(file_list: list) -> list:
    """The core of the second stage of the program."""
    valid = True
    while valid:
        path = input()
        if path.startswith('A'):
            print_object(file_list)
            valid = False
        elif path.startswith('N '):
            result = command_n(file_list, path[2:])
            valid = False
        elif path.startswith('E '):
            result = command_e(file_list, path[2:])
            valid = False
        elif path.startswith('T '):
            result = command_t(file_list, path[2:])
            valid = False
        elif path.startswith('< ') and path[2:].isdigit() and int(path[2:]) >= 0:
            result = command_smaller(file_list, int(path[2:]))
            valid = False
        elif path.startswith('> ') and path[2:].isdigit() and int(path[2:]) >= 0:
            result = command_bigger(file_list, int(path[2:]))
            valid = False
        else:
            _print_object("ERROR")
    _print_object(result)
    return result


def _third_stage(result: list) -> None:
    """The final stage of the program."""
    valid = True
    while valid:
        action = input()
        if action == 'F':
            command_f(result)
            valid = False
        elif action == 'D':
            command_copy(result)
            valid = False
        elif action == 'T':
            command_time(result)
            valid = False
        else:
            _print_object("ERROR")


def start_program() -> None:
    """The main dashboard of the program."""
    files = _first_stage()
    result = _second_stage(files)
    if result != []:
        _third_stage(result)


if __name__ == "__main__":
    start_program()
