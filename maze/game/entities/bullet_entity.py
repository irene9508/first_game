import pygame
from Box2D import b2FixtureDef, b2CircleShape

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
        self.body = self.game.world.CreateDynamicBody()
        fixture_def = b2FixtureDef(shape=b2CircleShape(radius=0.1), isSensor=True)
        fixture = self.body.CreateFixture(fixture_def)

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

    def render(self, surface, render_scale):
        bullet = pygame.transform.rotate(self.sprite, self.rotation)
        width, height = bullet.get_size()[0], bullet.get_size()[1]
        bullet = pygame.transform.smoothscale(
            bullet, (int(width * render_scale[0]), int(height * render_scale[1])))
        surface.blit(bullet, (int((self.x - width / 2) * render_scale[0]),
                              int((self.y - height / 2) * render_scale[1])))
        super().render(surface, render_scale)

    def trigger_collision_reaction(self, enemy):
        self.marked_for_destroy = True
        enemy.health -= 1
        print(enemy.health)

    def synchronize_body(self):  # entity gives new info to body
        self.body.position = (self.x * self.game.physics_scale,
                              self.y * self.game.physics_scale)

    def synchronize_entity(self):  # body gives new info to entity
        self.x = self.body.position[0] / self.game.physics_scale
        self.y = self.body.position[1] / self.game.physics_scale
