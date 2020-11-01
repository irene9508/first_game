from maze.game.entities.entity import Entity
import pygame


class BulletEntity(Entity):
    def __init__(self, game, x, y, rotation):
        super().__init__(game)
        self.bullet = pygame.image.load("data/images/bullet.png")
        self.rotation = rotation
        self.x = x
        self.y = y

    def update(self, delta_time):
        speed = 500
        if self.rotation == 0:
            self.y -= speed * delta_time
        if self.rotation == 90:
            self.x -= speed * delta_time
        if self.rotation == 180:
            self.y += speed * delta_time
        if self.rotation == 270:
            self.x += speed * delta_time
        if 600 < self.y < 0 or 800 < self.x < 0:
            self.marked_for_destroy = True

    def render(self, surface):
        bullet = pygame.transform.rotate(self.bullet, self.rotation)
        width = bullet.get_size()[0]
        height = bullet.get_size()[1]
        if self.rotation == 0:
            surface.blit(bullet, (int(self.x - width / 2),
                                  int(self.y - height / 2) - 100))

        if self.rotation == 90:
            surface.blit(bullet, (int(self.x - width / 2) - 100,
                                  int(self.y - height / 2)))
        if self.rotation == 180:
            surface.blit(bullet, (int(self.x - width / 2),
                                  int(self.y - height / 2) + 100))
        if self.rotation == 270:
            surface.blit(bullet, (int(self.x - width / 2) + 100,
                                  int(self.y - height / 2)))

