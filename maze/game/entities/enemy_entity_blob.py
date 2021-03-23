import pygame

from pygame import image as img
from maze.game.entities.enemy_entity import EnemyEntity


class EnemyEntityBlob(EnemyEntity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 10

        # animation:
        self.img_left = [img.load("data/images/e1/e1l1.png").convert_alpha()]
        self.img_right = [img.load("data/images/e1/e1r1.png").convert_alpha()]
        self.img_up = [img.load("data/images/e1/e1u1.png").convert_alpha()]
        self.img_down = [img.load("data/images/e1/e1d1.png").convert_alpha()]
        self.img_dead = [img.load("data/images/e1/e1dead.png").convert_alpha()]
        self.img_dead_near = [img.load("data/images/e1/e1dead_near.png").convert_alpha()]
        self.images = self.img_down
