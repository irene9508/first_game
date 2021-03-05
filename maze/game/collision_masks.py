from enum import IntFlag, auto


class Category(IntFlag):
    CHARACTER_BULLET = auto()
    ENEMY_BULLET = auto()
    CHARACTER = auto()
    CORPSE = auto()
    ENEMY = auto()
    WALL = auto()
