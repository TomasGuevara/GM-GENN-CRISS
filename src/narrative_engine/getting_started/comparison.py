from enum import Enum

class Comparison(str, Enum):
    EQUAL = "__eq__"
    NOT_EQUAL = "__ne__"
    GREATER = "__gt__"
    GREATER_EQUAL = "__ge__"
    LESS = "__lt__"
    LESS_EQUAL = "__le__"