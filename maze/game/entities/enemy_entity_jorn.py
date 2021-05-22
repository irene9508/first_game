import pygame

from maze.game.entities.enemy_entity import EnemyEntity
from pygame.transform import flip
from pygame import image as img

class EnemyEntityJorn(EnemyEntity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 15

        # animation:
        self.img_l1 = [pygame.image.load("data/images/e1/e2l1.png").convert_alpha()]
        self.img_r1 = [flip(img.load("data/images/e1/e2l1.png").convert_alpha(), True, False)]
        self.img_up = [pygame.image.load("data/images/e1/e2l1.png").convert_alpha()]
        self.img_down = [pygame.image.load("data/images/e1/e2r1.png").convert_alpha()]
        self.img_dead = [pygame.image.load("data/images/e1/e1dead.png").convert_alpha()]
        self.images = self.img_down
