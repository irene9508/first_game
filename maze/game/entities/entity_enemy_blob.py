from maze.game.entities.entity_enemy import EntityEnemy
import pygame


class EntityEnemyBlob(EntityEnemy):
    def __init__(self, game):
        super().__init__(game)

        self.sprites_left = [pygame.image.load("data/images/enemy1/e1l1.png")]
        self.sprites_right = [pygame.image.load("data/images/enemy1/e1r1.png")]
        self.sprites_up = [pygame.image.load("data/images/enemy1/e1u1.png")]
        self.sprites_down = [pygame.image.load("data/images/enemy1/e1d1.png")]

        self.health = 10
        self.collision_rect_solid = pygame.Rect(-99, 20, 198, 69)
        self.collision_rect_trigger = pygame.Rect(-100, -90, 200, 180)
