#
# Purpur Tentakel
# langauge files
# 18.06.2023
#

# python
import os
import shutil

# libs
import json
import sqlite3

# me
import Print as p
import files


def export(languages: list[str, ...], jsons: list) -> None:
    for i in range(len(jsons)):
        language: str = languages[i + 1].lower() + "." + files.jsons_ending
        file = os.path.join(files.jsons_directory, language)
        ex = json.dumps(jsons[i], indent=4)
        files.export(ex, file)


def delete() -> None:
    if not os.path.exists(files.jsons_directory):
        p.Print(f"no files deleted because directory ({files.jsons_directory}) does not exist", p.PrintType.INFO)
        return

    file_list: list = [f for f in os.listdir(files.jsons_directory)]
    if len(file_list) == 0:
        p.Print(f"no files deleted because no files existrs in dorectory: {files.jsons_directory}", p.PrintType.INFO)
        return;

    for f in file_list:
        file = os.path.join(files.jsons_directory, f)

        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

        p.Print(f"deleting {file}", p.PrintType.INFO)


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
    file_name: str = files.db_name
    if not os.path.exists(file_name):
        p.Print(f"{file_name} is not existing", p.PrintType.ERROR)
        p.Print("exiting...", p.PrintType.FINISH)

    else:
        con = sqlite3.connect(file_name)
        cur = con.cursor()

        loaded: list = load(cur)
        generated: list = generate(loaded)
        delete()
        export(loaded[0], generated)
        p.Print("all languages generated", p.PrintType.FINISH)

    input()