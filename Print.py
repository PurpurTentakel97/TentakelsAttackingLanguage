#
# Purpur Tentakel
# 07.04.2023
#

from enum import Enum


class PrintType(Enum):
    INFO = "[INFO]",
    ERROR = "[ERROR]",
    FINISH = "[FINISH]",
    SUCCESS = "[SUCCESS]",


def Print(message: str, type: PrintType) -> None:
    longest: int = len(PrintType.SUCCESS.value[0])  # enter the longest enum here
    print(f"{' ' * (longest - len(type.value[0]))}{type.value[0]} {message}")


def Print_With_Level(message: str, type: PrintType, level: int):
    message = '|' * (level + 1) + ' ' + message
    Print(message, type)
