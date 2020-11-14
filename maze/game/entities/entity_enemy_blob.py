from maze.game.entities.entity_enemy import EntityEnemy
import pygame


class EntityEnemyBlob(EntityEnemy):
    def __init__(self, game):
        super().__init__(game)

        self.sprites_left = [pygame.image.load("data/images/enemy1/e1l1.png").convert_alpha()]
        self.sprites_right = [pygame.image.load("data/images/enemy1/e1r1.png").convert_alpha()]
        self.sprites_up = [pygame.image.load("data/images/enemy1/e1u1.png").convert_alpha()]
        self.sprites_down = [pygame.image.load("data/images/enemy1/e1d1.png").convert_alpha()]

        self.width = self.sprites_left[0].get_size()[0]
        self.height = self.sprites_left[0].get_size()[1]
        self.health = 10
        self.collision_rect_solid = pygame.Rect(-(self.width/2), 15, self.width, 30)
        self.collision_rect_trigger = pygame.Rect(-(self.width/2),
                                                  -(self.height/2),
                                                  self.width, self.height)
