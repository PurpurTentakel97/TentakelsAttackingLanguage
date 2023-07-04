#
# Purpur Tentakel
# 07.04.2023
#

from enum import Enum


# @formatter:off
class PrintType(Enum):
    INFO =       "[INFO]",
    ERROR =      "[ERROR]",
    FINISH =     "[FINISH]",
    DELETING =   "[DELETING]",
    EXPORTING =  "[EXPORTING]",
# @formatter:on


def Print(message: str, type: PrintType) -> None:
    longest: int = len(PrintType.EXPORTING.value[0])  # enter the longest enum here
    print(f"{' ' * (longest - len(type.value[0]))}{type.value[0]} {message}")


def Print_With_Level(message: str, type: PrintType, level: int):
    message = '|' * (level + 1) + ' ' + message
    Print(message, type)
