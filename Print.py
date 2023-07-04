#
# Purpur Tentakel
# add
# 07.04.2023
#

from enum import Enum



class PrintType(Enum):
    INFO = "[INFO]",
    ERROR = "[ERROR]",
    FINISH =  "[FINISH]",


def Print(message: str, type: PrintType) -> None:
    longest: int = len(PrintType.FINISH.value[0]) # enter the longest enum here
    print(f"{type.value[0]}{' ' * (longest - len(type.value[0]))} {message}")
