from enum import IntEnum, StrEnum


class FindConditions(IntEnum):
    CLASS_NAME = 0
    TITLE = 1
    PROCESS_NAME = 2
    PROCESS_ID = 3


class MouseButtons(StrEnum):
    LEFT = "LEFT"
    MIDDLE = "MIDDLE"
    RIGHT = "RIGHT"
