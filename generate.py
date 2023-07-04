#
# Purpur Tentakel
# generate langauge files from the db
# Python 3.11
# 18.06.2023
#

# python
import os

# libs
import json
import sqlite3

# me
from helper import files
from helper import Quit as q
from helper import Print as p


def export(languages: list[str, ...], jsons: list) -> bool:
    valid: bool = True
    for i in range(len(jsons)):
        language: str = languages[i + 1].lower() + "." + files.jsons_ending
        ex = json.dumps(jsons[i], indent=4)
        if not files.export(ex, language, files.jsons_directory):
            valid = False

    if not valid:
        return False

    return True


def generate(data: list) -> list:
    dicts: list = list()
    languages: tuple = data[0]
    for i in range(len(languages) - 1):
        dicts.append(dict())
    for line_id in range(1, len(data)):
        line: tuple = data[line_id]
        for entry_id in range(1, len(line)):
            dicts[entry_id - 1][line[0]] = line[entry_id]

    return dicts


def load(cur) -> list:
    sql_command: str = """SELECT * FROM main"""
    data: list = cur.execute(sql_command).fetchall()
    return data


if __name__ == "__main__":
    file_name: str = files.db_full_default_name
    if not os.path.exists(file_name):
        q.Quit(f"{file_name} is not existing")

    con = sqlite3.connect(file_name)
    cur = con.cursor()

    loaded: list = load(cur)
    generated: list = generate(loaded)
    p.Print("files in export directory", p.PrintType.DELETING)
    if not files.delete_all_in_directory(files.jsons_directory):
        q.Quit("not all files could be deleted")
    p.Print("new files", p.PrintType.EXPORTING)
    if not export(loaded[0], generated):
        q.Quit("not all files could be generated")
    p.Print("all languages generated", p.PrintType.FINISH)

    input()
