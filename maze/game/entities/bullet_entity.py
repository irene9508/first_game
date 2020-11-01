from maze.game.entities.entity import Entity
import pygame


class BulletEntity(Entity):
    def __init__(self, game, x, y):
        super().__init__(game)
        self.bullet_up = pygame.image.load("data/images/bullet_up.png")
        self.x = x
        self.y = y

    def update(self, delta_time):
        self.y -= 250 * delta_time
        if self.y < 0:
            self.marked_for_destroy = True

    def render(self, surface):
        surface.blit(self.bullet_up, (int(self.x + 70), int(self.y - 20)))
