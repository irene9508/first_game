import pygame

from maze.game.entities.enemy_entity import EnemyEntity


class EnemyEntityJorn(EnemyEntity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 15

        # animation:
        self.sprites_left = [
            pygame.image.load("data/images/e1/e2l1.png").convert_alpha()]
        self.sprites_right = [
            pygame.image.load("data/images/e1/e2r1.png").convert_alpha()]
        self.sprites_up = [
            pygame.image.load("data/images/e1/e2l1.png").convert_alpha()]
        self.sprites_down = [
            pygame.image.load("data/images/e1/e2r1.png").convert_alpha()]
        self.sprites = self.sprites_down
