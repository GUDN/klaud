from enum import Flag, auto


class Scopes(Flag):
    NONE = 0
    MASTER = auto()
    MANAGE = auto()
    READ = auto()
    WRITE = auto()
