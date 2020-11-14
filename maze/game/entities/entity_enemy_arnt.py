from maze.game.entities.entity_enemy import EntityEnemy
import pygame


class EntityEnemyArnt(EntityEnemy):
    def __init__(self, game):
        super().__init__(game)

        # properties:
        self.health = 8

        # animation:
        self.sprites_left = [pygame.image.load("data/images/enemy1/e3r1.png").convert_alpha()]
        self.sprites_right = [pygame.image.load("data/images/enemy1/e3r1.png").convert_alpha()]
        self.sprites_up = [pygame.image.load("data/images/enemy1/e3r1.png").convert_alpha()]
        self.sprites_down = [pygame.image.load("data/images/enemy1/e3r1.png").convert_alpha()]
