from maze.game.entities.entity_enemy import EntityEnemy
import pygame


class EntityEnemyArnt(EntityEnemy):
    def __init__(self, game):
        super().__init__(game)

        self.sprites_left = [pygame.image.load("data/images/enemy1/e2l1.png")]
        self.sprites_right = [pygame.image.load("data/images/enemy1/e2r1.png")]
        self.sprites_up = [pygame.image.load("data/images/enemy1/e2l1.png")]
        self.sprites_down = [pygame.image.load("data/images/enemy1/e2r1.png")]

        self.health = 15
