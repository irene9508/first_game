from maze.game.entities.entity_enemy import EntityEnemy
import pygame


class EntityEnemyBlob(EntityEnemy):  # 109x93
    def __init__(self, game):
        super().__init__(game)

        # properties:
        self.health = 10

        # animation:
        self.sprites_left = [pygame.image.load("data/images/enemy1/e1l1.png").convert_alpha()]
        self.sprites_right = [pygame.image.load("data/images/enemy1/e1r1.png").convert_alpha()]
        self.sprites_up = [pygame.image.load("data/images/enemy1/e1u1.png").convert_alpha()]
        self.sprites_down = [pygame.image.load("data/images/enemy1/e1d1.png").convert_alpha()]

        # collisions:
        self.solid_collision_box = pygame.Rect(-55, 15, 109, 30)
        self.trigger_collision_box = pygame.Rect(-55, -46, 109, 93)