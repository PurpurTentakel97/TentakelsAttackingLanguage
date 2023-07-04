#
# Purpur Tentakel
# 07.04.2023
#

from datetime import datetime

long_file_date: str = "%Y_%m_%d_%H_%M_%S"


def get_current_time_as_string(format_: str) -> str:
    return datetime.now().strftime(format_)
