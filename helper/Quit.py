#
# Purpur Tentakel
# add a language to the db
# Python 3.11
# 07.04.2023
#

# me
from helper import Print as p


def Quit(message: str) -> None:
    p.Print(message, p.PrintType.ERROR)
    p.Print("exiting...", p.PrintType.FINISH)
    input()
    quit()
