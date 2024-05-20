from enum import Enum


class Position(str, Enum):
    GK = "GK"
    Fixed = "Fixed"
    Pivot = "Pivot"
