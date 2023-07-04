#
# Purpur Tentakel
# 07.04.2023
#
import json
# python
import os
import shutil

# me
from helper import date
from helper import Print as p

# globals
jsons_directory: str = "jsons"
new_json_directory: str = "new_jsons"
jsons_ending: str = "tal"

db_name: str = "language"
db_ending: str = "db"
db_full_default_name: str = db_name + '.' + db_ending
db_copy_dir: str = "old_database"

copy_addon: str = "old"


def load_json(filename: str, file_ending: str, level: int = 0) -> tuple:
    p.Print_With_Level(f"{filename}", p.PrintType.LOADING, level)

    if not os.path.exists(filename):
        p.Print_With_Level(f"{filename} does not exist", p.PrintType.ERROR, level)
        return False, None

    if not os.path.isfile(filename):
        p.Print_With_Level(f"{filename} is no file", p.PrintType.ERROR, level)
        return False, None

    body, tail = os.path.splitext(filename)
    if tail != '.' + file_ending:
        p.Print_With_Level(f"{filename} does not has the {'.' + file_ending} format", p.PrintType.ERROR, level)
        return False, None

    with open(filename, "r") as file:
        try:
            data: list = json.load(file)
            return True, data
        except json.JSONDecodeError as e:
            message: str = f"pos: {e.pos} | line: {e.lineno} | column: {e.colno} | msg: {e.msg}"
            p.Print_With_Level(f"JSON error: {message}", p.PrintType.ERROR, level)
        except:
            p.Print_With_Level(f"unknown error while loading {filename}", p.PrintType.ERROR, level)

    return False, None


def generate_dir_if_not_existing(dirname: str, level: int = 0) -> None:
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        p.Print_With_Level(f"generated directory {dirname}", p.PrintType.INFO, level)


def is_file_existing(filename: str, level: int = 0) -> bool:
    if not os.path.exists(filename):
        p.Print_With_Level(f"{filename} not existing", p.PrintType.ERROR, level)
        return False

    if not os.path.isfile(filename):
        p.Print_With_Level(f"{filename} is no file", p.PrintType.ERROR, level)
        return False

    return True


def copy_file(filename: str, dest_dir: str, level: int = 0) -> bool:
    p.Print_With_Level(filename, p.PrintType.COPYING, level)

    if not os.path.exists(filename):
        p.Print_With_Level(f"file {filename} not existing", p.PrintType.ERROR, level)
        return False

    if not os.path.isfile(filename):
        p.Print_With_Level(f"{filename} is no file", p.PrintType.ERROR, level)
        return False

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        p.Print_With_Level(f"generated directory {dest_dir}", p.PrintType.INFO, level)

    elif not os.path.isdir(dest_dir):
        p.Print_With_Level(f"{dest_dir} is not a directory", p.PrintType.ERROR, level)
        return False

    base, tail = os.path.splitext(filename)
    new_filename: str = base + "_" + copy_addon + "_" + date.get_current_time_as_string(date.long_file_date) + tail
    new_filename = os.path.join(dest_dir, new_filename)

    shutil.copyfile(filename, new_filename)

    return True


def export(content: str, filename: str, dest_dir: str, level: int = 0) -> bool:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        p.Print_With_Level(f"generated directory {dest_dir}", p.PrintType.INFO, level)

    filename = os.path.join(dest_dir, filename)
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
