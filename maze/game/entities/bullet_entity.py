from maze.game.entities.entity import Entity
import pygame
import time


class BulletEntity(Entity):
    def __init__(self, game, x, y):
        super().__init__(game)
        self.image = pygame.image.load("data/images/bullet2.png")
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 1

    def update(self):
        self.y -= 1
        if self.y < 0:
            self.marked_for_destroy = True

    def render(self, surface):
        surface.blit(self.image, (int(self.x + 70), int(self.y - 20)))


# <maze.game.entities.character_entity.CharacterEntity object at 0x038A9A60>

# V in render, blit the image on the screen
# V in update, make the bullet move
# V in update, if bullet is out of the screen, mark it for destroy
# and magic happens
#
