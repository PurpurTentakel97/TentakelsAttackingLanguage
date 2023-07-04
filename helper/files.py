#
# Purpur Tentakel
# 07.04.2023
#

# python
import os

# me
from helper import files
from helper import Print as p

# globals
jsons_directory: str = "jsons"
jsons_ending: str = "tal"

db_name: str = "language"
db_ending: str = "db"
db_full_default_name: str = db_name + '.' + db_ending
db_copy_addon: str = "old"


def copy_file(filename: str, level: int = 0) -> bool:
    p.Print_With_Level(filename, p.PrintType.COPYING, level)

    if not os.path.exists(filename):
        p.Print_With_Level(f"file {filename} not existing", p.PrintType.ERROR, level)
        return False


def export(content: str, filename: str, level: int = 0) -> bool:
    if not os.path.exists(files.jsons_directory):
        os.mkdir(files.jsons_directory)
        p.Print_With_Level(f"generated directory {files.jsons_directory}", p.PrintType.INFO, level)

    p.Print_With_Level(f"{filename}", p.PrintType.EXPORTING, level)
    with open(filename, "w") as f:
        f.write(content)

    if not os.path.exists(filename):
        p.Print("generated file not existing", p.PrintType.ERROR)
        return False

    return True


def delete_file(file: str, level: int = 0) -> bool:
    p.Print_With_Level(f"{file}", p.PrintType.DELETING, level)

    if not os.path.exists(file):
        p.Print_With_Level(f"no file {file} exists for deleting", p.PrintType.ERROR, level)
        return False

    try:
        os.remove(file)
    except OSError:
        p.Print_With_Level(f"unable to delete file {file}", p.PrintType.ERROR, level)
        return False

    return True


def delete_empty_directory(directory: str, level: int = 0) -> bool:
    p.Print_With_Level(f"{directory}", p.PrintType.DELETING, level)

    if not os.path.exists(directory):
        p.Print_With_Level(f"no directory {directory} exists for deleting", p.PrintType.ERROR, level)
        return False

    if len(os.listdir(directory)) > 0:
        p.Print_With_Level(f"directory {directory} still has entries", p.PrintType.ERROR, level)
        return False

    try:
        os.rmdir(directory)
    except OSError:
        p.Print_With_Level(f"unable to delete directory {directory}", p.PrintType.ERROR, level)
        return False

    return True


def delete_all_in_directory(directory: str, level: int = 0) -> bool:
    if not os.path.exists(directory):
        p.Print_With_Level(f"no files deleted because directory ({directory}) does not exist", p.PrintType.INFO, level)
        return False

    file_list: list = [f for f in os.listdir(directory)]
    if len(file_list) == 0:
        p.Print_With_Level(f"no files deleted because no files exists in directory: {directory}", p.PrintType.INFO,
                           level)
        return False

    valid: bool = True
    for f in file_list:
        file = os.path.join(directory, f)

        if os.path.isfile(file):
            if not delete_file(file, level):
                valid = False
        elif os.path.isdir(file):
            if len(os.listdir(file)) > 0:
                if not delete_all_in_directory(file, level + 1):
                    valid = False
            if not delete_empty_directory(file, level):
                valid = False

    if not valid:
        return False

    return True
