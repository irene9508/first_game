import pygame

from maze.game.entities.entity import Entity


class BulletEntity(Entity):  # 25x25
    def __init__(self, game, x, collision_group, y, rotation):
        super().__init__(game)

        # properties:
        self.rotation = rotation
        self.x = x
        self.y = y

        # collisions:
        self.trigger = True
        self.collision_group = collision_group
        self.hitbox = pygame.Rect(-12, -12, 25, 25)

        # other:
        self.sprite = pygame.image.load(
            "data/images/bullet.png").convert_alpha()

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

    def render(self, surface, scale):
        bullet = pygame.transform.rotate(self.sprite, self.rotation)
        width, height = bullet.get_size()[0], bullet.get_size()[1]
        bullet = pygame.transform.smoothscale(bullet, (int(width * scale[0]),
                                                       int(height * scale[1])))
        surface.blit(bullet, (int((self.x - width / 2) * scale[0]),
                              int((self.y - height / 2) * scale[1])))
        super().render(surface, scale)

    def trigger_collision_reaction(self, enemy):
        self.marked_for_destroy = True
        enemy.health -= 1
        print(enemy.health)
