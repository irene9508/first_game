from enum import IntFlag, auto


class Category(IntFlag):
    CHARACTER_BULLET = auto()
    ENEMY_BULLET = auto()
    CHARACTER = auto()
    ENEMY = auto()
    WALL = auto()
