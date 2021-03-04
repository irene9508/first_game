import pygame

from maze.game.entities.enemy_entity import EnemyEntity


class EnemyEntityArnt(EnemyEntity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 8

        # animation:
        self.sprites_left = [
            pygame.image.load("data/images/e1/e3r1.png").convert_alpha()]
        self.sprites_right = [
            pygame.image.load("data/images/e1/e3r1.png").convert_alpha()]
        self.sprites_up = [
            pygame.image.load("data/images/e1/e3r1.png").convert_alpha()]
        self.sprites_down = [
            pygame.image.load("data/images/e1/e3r1.png").convert_alpha()]
        self.sprites_dead = [
            pygame.image.load("data/images/e1/e1dead.png").convert_alpha()]
        self.sprites = self.sprites_down
