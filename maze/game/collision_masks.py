from enum import IntFlag, auto


class Category(IntFlag):
    CHARACTER = auto()
    CHARACTER_BULLET = auto()
    ENEMY = auto()
    ENEMY_BULLET = auto()
    WALL = auto()
