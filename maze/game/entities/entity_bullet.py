from maze.game.entities.entity import Entity
import pygame


class EntityBullet(Entity):
    def __init__(self, game, x, collision_group, y, rotation):
        super().__init__(game)
        self.sprite = pygame.image.load("data/images/bullet.png")
        self.collision_group = collision_group
        self.collision_rect_trigger = pygame.Rect(-25, -25, 50, 50)
        self.rotation = rotation
        self.trigger = True
        self.x = x
        self.y = y

    def update(self, delta_time):
        # movement direction:
        speed = 500
        if self.rotation == 0:
            self.y -= speed * delta_time
        if self.rotation == 90:
            self.x -= speed * delta_time
        if self.rotation == 180:
            self.y += speed * delta_time
        if self.rotation == 270:
            self.x += speed * delta_time

        # destruction:
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
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
