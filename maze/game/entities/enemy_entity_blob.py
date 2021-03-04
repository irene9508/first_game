import pygame

from maze.game.entities.enemy_entity import EnemyEntity


class EnemyEntityBlob(EnemyEntity):  # 109x93
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 10

        # animation:
        self.sprites_left = [
            pygame.image.load("data/images/e1/e1l1.png").convert_alpha()]
        self.sprites_right = [
            pygame.image.load("data/images/e1/e1r1.png").convert_alpha()]
        self.sprites_up = [
            pygame.image.load("data/images/e1/e1u1.png").convert_alpha()]
        self.sprites_down = [
            pygame.image.load("data/images/e1/e1d3.png").convert_alpha()]
        self.sprites_dead = [
            pygame.image.load("data/images/e1/e1dead.png").convert_alpha()]
        self.sprites = self.sprites_down
