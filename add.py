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

# me
from helper import files
from helper import Quit as q
from helper import Print as p


# load json
# add column to db named as json file
# add entries to db

def is_quit_input(input_: str) -> bool:
    return input_.strip() == 'q'


if __name__ == "__main__":
    p.Print("backup database", p.PrintType.COPYING)
    if not files.copy_file(files.db_full_default_name, files.db_copy_dir):
        q.Quit("not able to generate a backup database")

    con = sqlite3.connect(files.db_full_default_name)
    cur = con.cursor()

    files.generate_dir_if_not_existing(files.new_json_directory)

    p.Print("enter 'q' to quit", p.PrintType.INFO)

    while True:
        print()
        p.Print("enter the json name to add in database", p.PrintType.INPUT)
        json_name: str = input()
        if is_quit_input(json_name):
            break
        filename = os.path.join(files.new_json_directory, json_name.strip() + '.' + files.jsons_ending)
        if not files.is_file_existing(filename):
            continue

        valid, data = files.load_json(filename, files.jsons_ending)
        if not valid:
            continue

        p.Print("success", p.PrintType.DEBUG)

    p.Print("shutting down...", p.PrintType.INFO)
    time.sleep(1)
