from enum import Enum

class Operation(str, Enum):
    SET = "set"
    INCREMENT = "increment"
    DECREMENT = "decrement"
    ADD = "add"
    REMOVE = "remove"
    TOGGLE = "toggle"