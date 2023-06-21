#
# Purpur Tentakel
# langauge files
# 18.06.2023
#

import sqlite3
import os
import time
import json


def export(languages: list[str, ...], jsons: list) -> None:
    directory: str = "jsons"
    if not os.path.exists(directory):
        os.mkdir(directory)
        print(f"[INFO] generated directory {directory}")

    for i in range(len(jsons)):
        language: str = languages[i + 1].lower() + ".tal"
        print(f"[INFO] exporting {language}")
        ex = json.dumps(jsons[i], indent=4)

        with open(f"{directory}/{language}", "w") as file:
            file.write(ex)


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
    file_name: str = "language.db"
    if not os.path.exists(file_name):
        print(f"[ERROR] {file_name} is not existing")
        print("[FINISHED] exiting...")

    else:
        con = sqlite3.connect(file_name)
        cur = con.cursor()

        loaded: list = load(cur)
        generated: list = generate(loaded)
        export(loaded[0], generated)
        print("[FINISHED] all languages generated")

    time.sleep(1)
