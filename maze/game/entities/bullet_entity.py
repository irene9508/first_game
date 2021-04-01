from math import cos, sin, pi

import pygame
from Box2D import b2FixtureDef, b2CircleShape

from pygame import image as img
from maze.game.collision_masks import Category
from maze.game.entities.entity import Entity
from maze.game.particle_effect import ParticleEffect
from maze.game.room_change_behavior import RoomChangeBehavior


class BulletEntity(Entity):  # 25x25
    def __init__(self, game, x, y, rotation, category, mask):
        super().__init__(game)

        self.room_change_behavior = RoomChangeBehavior.destroy
        self.rotation = rotation
        self.x = x
        self.y = y

        # image:
        if category == Category.ENEMY_BULLET:
            self.img = img.load("data/images/bullet.png").convert_alpha()
        else:
            self.img = img.load("data/images/bullet1.png").convert_alpha()

        # collisions:
        position = (self.x * game.physics_scale, self.y * game.physics_scale)
        self.body = self.game.world.CreateDynamicBody(position=position, userData=self)
        fixt_def = b2FixtureDef(shape=b2CircleShape(radius=0.1), isSensor=True,
                                categoryBits=category, maskBits=mask)
        # noinspection PyUnusedLocal
        fixture = self.body.CreateFixture(fixt_def)
        self.velocity = [0, 0]

        # add particles:
        self.particle_effect = ParticleEffect(self.x, self.y, (190, 190, 190),
                                              0.08, [1, 10], [1, 15], 0, 50)

    def contact(self, fixture, other_fixture, contact):
        from maze.game.entities.enemy_entity import EnemyEntity
        from maze.game.entities.character_entity import CharacterEntity

        self.marked_for_destroy = True
        if isinstance(other_fixture.body.userData, EnemyEntity):
            EnemyEntity.take_damage(other_fixture.body.userData, 2)

        if isinstance(other_fixture.body.userData, CharacterEntity):
            other_fixture.body.userData.health -= 10

    def destroy(self):
        self.game.world.DestroyBody(self.body)

    def render(self, surface, r_scale):
        # particles:
        self.particle_effect.render(surface, r_scale)

        # bullet:
        bullet = pygame.transform.rotate(self.img, self.rotation)
        width, height = bullet.get_size()[0], bullet.get_size()[1]
        r_size = (int(width * r_scale[0]), int(height * r_scale[1]))
        bullet = pygame.transform.smoothscale(bullet, r_size)
        r_position = (int((self.x - width / 2) * r_scale[0]),
                      int((self.y - height / 2) * r_scale[1]))
        surface.blit(bullet, r_position)

        # parent:
        super().render(surface, r_scale)

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

    def update(self, delta_time):
        # movement direction:
        speed = 500
        self.velocity = [0, 0]
        self.velocity[0] = speed * cos(self.rotation * pi / 180)
        self.velocity[1] = speed * sin(self.rotation * pi / 180)

        # particles:
        self.particle_effect.x = self.x
        self.particle_effect.y = self.y
        self.particle_effect.update(delta_time)

        # destruction:
        if self.x < 0 or self.x > 1280 or self.y < 0 or self.y > 720:
            self.marked_for_destroy = True
