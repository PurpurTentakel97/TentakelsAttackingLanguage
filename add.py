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


# add column to db named as json file
# add entries to db

def _is_quit_input(input_: str) -> bool:
    return input_.strip() == 'q'


def _get_data_from_db(cur: Cursor) -> tuple[bool, list[tuple]]:
    sql_command: str = """SELECT * FROM main;"""
    try:
        cur.execute(sql_command)
        return True, cur.fetchall()
    except sqlite3.OperationalError as e:
        p.Print_SQLite_Error(f"{e.sqlite_errorcode} | {e.sqlite_errorname}")
        return False, list()


def _is_language_in_data(data: list, language: str) -> bool:
    if len(data) == 0:
        return False
    return language in data[0]


def _add_column(cur: Cursor, language: str) -> bool:
    sql_command: str = f"""ALTER TABLE main ADD COLUMN {language} TEXT;"""
    try:
        cur.execute(sql_command)
        p.Print(f"added column '{language}'", p.PrintType.INFO)
        _update_field(cur, language, language, "key")
        cur.connection.commit()
        return True
    except sqlite3.OperationalError as e:
        p.Print_SQLite_Error(f"{e.sqlite_errorcode} | {e.sqlite_errorname}")
        return False


def _update_field(cur: Cursor, language: str, value: str, key: str) -> None:
    sql_command: str = f"""UPDATE main SET {language} = ? WHERE key = ?;"""
    try:
        cur.execute(sql_command, (value, key))
        p.Print(f"updated '{value}' at '{key}'", p.PrintType.INFO)
    except sqlite3.OperationalError as e:
        p.Print_SQLite_Error(f"{e.sqlite_errorcode} | {e.sqlite_errorname}")
        p.Print(f"failed to update '{value}' at '{key}'", p.PrintType.ERROR)


def _update(o_cur: Cursor, o_data: list, n_data: list, language: str) -> None:
    if not _is_language_in_data(o_data, language):
        if not _add_column(o_cur, language):
            p.Print("failed to add new column", p.PrintType.ERROR)
            return

    l_index: int = n_data[0].index(language)
    k_index: int = 0

    for entry in n_data:
        if n_data.index(entry) == 0:
            continue
        if entry[k_index] is None:
            p.Print("key is is None", p.PrintType.ERROR)
            continue
        if entry[l_index] is None:
            p.Print(f"value is None for key '{entry[k_index]}'", p.PrintType.ERROR)
            continue

        _update_field(o_cur, language, entry[l_index], entry[k_index])


if __name__ == "__main__":

    # check database files
    if not files.is_file_existing(files.db_full_default_name):
        q.Quit(f"original database {files.db_full_default_name} doesn't exists")

    if not files.is_file_existing(files.db_full_new_name):
        q.Quit(f"new database {files.db_full_new_name} doesn't exists")

    # backup database
    p.Print("backup database", p.PrintType.COPYING)
    if not files.copy_file(files.db_full_default_name, files.db_copy_dir):
        q.Quit("not able to generate a backup database")

    # get con an cur
    o_con: Connection = sqlite3.connect(files.db_full_default_name)
    o_cur: Cursor = o_con.cursor()
    n_con: Connection = sqlite3.connect(files.db_full_new_name)
    n_cur: Cursor = n_con.cursor()

    # get data
    valid, o_data = _get_data_from_db(o_cur)
    if not valid:
        o_con.close()
        n_con.close()
        q.Quit(f"invalid data in {files.db_full_default_name}")

    valid, n_data = _get_data_from_db(n_cur)
    if not valid:
        o_con.close()
        n_con.close()
        q.Quit(f"invalid data in {files.db_full_new_name}")

    p.Print("enter 'q' to quit", p.PrintType.INFO)

    while True:
        # get input
        p.Print("enter the language that should get copied", p.PrintType.INPUT)
        language: str = input()

        # check quit
        if _is_quit_input(language):
            break

        # is valid language
        if not _is_language_in_data(n_data, language):
            p.Print(f"chosen language {language} is not in database {files.db_full_new_name}", p.PrintType.ERROR)
            continue

        if _is_language_in_data(o_data, language):
            p.Print(f"should {language} be overwritten? y | n", p.PrintType.INPUT)
            overwrite_input: str = input()
            if overwrite_input != 'y':
                p.Print("breaking...", p.PrintType.INFO)
                continue

        # update
        _update(o_cur, o_data, n_data, language)

        # save and reload
        p.Print("contain the chances? y | n", p.PrintType.INPUT)
        contain_input: str = input()
        if contain_input == 'y':
            p.Print("saved", p.PrintType.FINISH)
            o_con.commit()
            p.Print("reload data", p.PrintType.INFO)
            valid, o_data = _get_data_from_db(o_cur)
            if not valid:
                o_con.close()
                n_con.close()
                q.Quit(f"invalid data in {files.db_full_default_name}")
        else:
            p.Print("rollback", p.PrintType.FINISH)
            o_con.rollback()

        p.Print("success", p.PrintType.DEBUG)

    p.Print("shutting down...", p.PrintType.INFO)
    o_con.close()
    n_con.close()
    time.sleep(1)
