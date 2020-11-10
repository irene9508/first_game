from maze.game.entities.entity import Entity
import pygame


class EntityBullet(Entity):
    def __init__(self, game, x, collision_group, y, rotation):
        super().__init__(game)
        self.sprite = pygame.image.load("data/images/bullet.png")
        self.collision_group = collision_group
        self.width = self.sprite.get_size()[0]
        self.height = self.sprite.get_size()[1]
        self.coll_rect_trigger = pygame.Rect(-(self.width/2), -(self.height/2),
                                             self.width, self.height)
        self.rotation = rotation
        self.trigger = True
        self.x = x
        self.y = y

    def update(self, delta_time):
        # movement direction:
        speed = 100
        if self.rotation == 0:
            self.y -= speed * delta_time
        if self.rotation == 90:
            self.x -= speed * delta_time
        if self.rotation == 180:
            self.y += speed * delta_time
        if self.rotation == 270:
            self.x += speed * delta_time

        # destruction:
        if self.x < 0 or self.x > 1280 or self.y < 0 or self.y > 720:
            self.marked_for_destroy = True

    def render(self, surface):
        bullet = pygame.transform.rotate(self.sprite, self.rotation)
        width, height = bullet.get_size()[0], bullet.get_size()[1]
        surface.blit(bullet, (int(self.x - width / 2),
                              int(self.y - height / 2)))
        super().render(surface)

    def solve_trigger_collision(self, enemy):
        self.marked_for_destroy = True
        enemy.health -= 1
