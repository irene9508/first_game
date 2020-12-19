import pygame

from Box2D import b2FixtureDef, b2CircleShape
from maze.game.entities.entity import Entity


class BulletEntity(Entity):  # 25x25
    def __init__(self, game, x, collision_group, y, rotation):
        super().__init__(game)

        # properties:
        self.img = pygame.image.load("data/images/bullet.png").convert_alpha()
        self.rotation = rotation
        self.x = x
        self.y = y

        # collisions:
        self.body = self.game.world.CreateDynamicBody(
            position=(self.x * self.game.physics_scale,
                      self.y * self.game.physics_scale),
            userData=self)
        fixt_def = b2FixtureDef(shape=b2CircleShape(radius=0.1), isSensor=True)
        fixt_def.filter.groupIndex = collision_group
        # noinspection PyUnusedLocal
        fixture = self.body.CreateFixture(fixt_def)
        self.velocity = [0, 0]

    def contact(self, fixture, other_fixture, contact):
        from maze.game.entities.enemy_entity import EnemyEntity

        self.marked_for_destroy = True
        if isinstance(other_fixture.body.userData, EnemyEntity):
            enemy = other_fixture.body.userData
            enemy.health -= 1

    def destroy(self):
        self.game.world.DestroyBody(self.body)

    def update(self, delta_time):
        # movement direction:
        speed = 100
        self.velocity = [0, 0]
        if self.rotation == 90:
            self.velocity[1] = -speed
        if self.rotation == 180:
            self.velocity[0] = -speed
        if self.rotation == 270:
            self.velocity[1] = speed
        if self.rotation == 0:
            self.velocity[0] = speed

        # destruction:
        if self.x < 0 or self.x > 1280 or self.y < 0 or self.y > 720:
            self.marked_for_destroy = True

    def render(self, surface, render_scale):
        bullet = pygame.transform.rotate(self.img, self.rotation)
        width, height = bullet.get_size()[0], bullet.get_size()[1]
        r_size = (int(width * render_scale[0]), int(height * render_scale[1]))
        bullet = pygame.transform.smoothscale(bullet, r_size)
        r_position = (int(((self.x - width / 2) * render_scale[0])),
                      int((self.y - height / 2) * render_scale[1]))

        surface.blit(bullet, r_position)
        super().render(surface, render_scale)

    def trigger_collision_reaction(self, enemy):
        self.marked_for_destroy = True
        enemy.health -= 1
        print(enemy.health)

    def synchronize_body(self):  # entity gives new info to body
        self.body.position = (self.x * self.game.physics_scale,
                              self.y * self.game.physics_scale)
        self.body.linearVelocity = (self.velocity[0] * self.game.physics_scale,
                                    self.velocity[1] * self.game.physics_scale)

    def synchronize_entity(self):  # body gives new info to entity
        self.x = self.body.position[0] / self.game.physics_scale
        self.y = self.body.position[1] / self.game.physics_scale
        self.velocity = [self.body.linearVelocity[0] / self.game.physics_scale,
                         self.body.linearVelocity[1] / self.game.physics_scale]
