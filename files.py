#
# Purpur Tentakel
# 07.04.2023
#

# python
import os

# me
import files
import Print as p

# globals
jsons_directory: str = "jsons"
jsons_ending: str = "tal"

db_name: str = "language.db"


def export(content: str, filename:str) -> None:
    if not os.path.exists(files.jsons_directory):
        os.mkdir(files.jsons_directory)
        p.Print(f"generated directory {files.jsons_directory}", p.PrintType.INFO)

    p.Print(f"exporting {filename}", p.PrintType.INFO)
    with open(filename, "w") as f:
        f.write(content)
