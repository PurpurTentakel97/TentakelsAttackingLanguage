#
# Purpur Tentakel
# add a language to the db
# Python 3.11
# 07.04.2023
#

# python
import time
import os.path

# lib
import sqlite3
from sqlite3 import Cursor
from sqlite3 import Connection

# me
from helper import files
from helper import Quit as q
from helper import Print as p


# load json
# add column to db named as json file
# add entries to db

def is_quit_input(input_: str) -> bool:
    return input_.strip() == 'q'


def is_language_in_db(cur: Cursor, language: str) -> bool:
    print(language)
    sql_command: str = f"""SELECT {language} FROM main;"""
    cur.execute(sql_command)
    print(cur.fetchall())

    return False
    # @todo fix language check


if __name__ == "__main__":
    p.Print("backup database", p.PrintType.COPYING)
    if not files.copy_file(files.db_full_default_name, files.db_copy_dir):
        q.Quit("not able to generate a backup database")

    con: Connection = sqlite3.connect(files.db_full_default_name)
    cur: Cursor = con.cursor()

    files.generate_dir_if_not_existing(files.new_json_directory)

    p.Print("enter 'q' to quit", p.PrintType.INFO)

    while True:
        # whitespace
        print()

        # get input
        p.Print("enter the json name to add in database", p.PrintType.INPUT)
        json_name: str = input()

        # check quit
        if is_quit_input(json_name):
            break
        # is existing file
        filename = os.path.join(files.new_json_directory, json_name.strip() + '.' + files.jsons_ending)
        if not files.is_file_existing(filename):
            continue

        # get json data
        valid, data = files.load_json(filename, files.jsons_ending)
        if not valid:
            continue

        # language already existing
        if is_language_in_db(cur, json_name):
            p.Print(f"language {json_name} already in database", p.PrintType.ERROR)
            continue

        p.Print("success", p.PrintType.DEBUG)

    p.Print("shutting down...", p.PrintType.INFO)
    time.sleep(1)
