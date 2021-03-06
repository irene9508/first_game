import random

import pygame
from Box2D import b2FixtureDef, b2CircleShape
from pygame import mixer

from maze.game.collision_masks import Category
from maze.game.entities.bullet_entity import BulletEntity
from maze.game.entities.entity import Entity
from maze.game.entities.particle_effect_entity import ParticleEffectEntity
from maze.game.room_change_behavior import RoomChangeBehavior


class CharacterEntity(Entity):
    def __init__(self, game):
        super().__init__(game)

        # animation:
        self.img_down = [
            pygame.image.load("data/images/e1/e1d1.png").convert_alpha()]
        self.img_left = [
            pygame.image.load("data/images/e1/e1l1.png").convert_alpha()]
        self.img_right = [
            pygame.image.load("data/images/e1/e1r1.png").convert_alpha()]
        self.img_up = [
            pygame.image.load("data/images/e1/e1u1.png").convert_alpha()]
        self.img_index = 0  # needed to iterate through the list of images
        self.images = self.img_down
        self.animation_length = 0.12  # controls speed of sprite animation

        # collisions:
        self.body = self.game.world.CreateDynamicBody(
            position=(self.x * self.game.physics_scale,
                      self.y * self.game.physics_scale),
            userData=self)
        fixt_def = b2FixtureDef(
            shape=b2CircleShape(radius=0.4),
            friction=0.2,
            density=1.0,
            categoryBits=Category.CHARACTER,
            maskBits=Category.ENEMY | Category.ENEMY_BULLET | Category.WALL |
            Category.CORPSE)
        # noinspection PyUnusedLocal
        fixture = self.body.CreateFixture(fixt_def)

        # properties:
        self.health = 100
        self.room_change_behavior = RoomChangeBehavior.nothing
        self.velocity = [0, 0]
        self.x = 280
        self.y = 300

        # other:
        self.initial_shot_timer = 0.1  # prevents the bullets from rapid firing
        self.shot_sound = mixer.Sound('data/sounds/laser.wav')
        # add particles:
        self.particle_effect = ParticleEffectEntity(self.x, self.y, (255, 0, 0),
            1)

    def destroy(self):
        self.game.world.DestroyBody(self.body)

    def update(self, delta_time):
        keys = pygame.key.get_pressed()

        # particle effect:
        self.particle_effect.x = self.x
        self.particle_effect.y = self.y
        self.particle_effect.update(delta_time, 0.2, random.randint(2, 15))

        # animation, used in render():
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.img_index += 1
            if self.img_index == len(self.images):
                self.img_index = 0
            self.animation_length = 0.12

        # movement:
        speed = 300
        self.velocity = [0, 0]
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.images = self.img_up
            self.velocity[1] = -speed
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.images = self.img_left
            self.velocity[0] = -speed
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.images = self.img_down
            self.velocity[1] = speed
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.images = self.img_right
            self.velocity[0] = speed

        # shooting:
        shot_timer = 0.2
        self.initial_shot_timer -= delta_time
        up, down = keys[pygame.K_UP], keys[pygame.K_DOWN]
        left, right = keys[pygame.K_LEFT], keys[pygame.K_RIGHT]
        if up and not down:
            self.images = self.img_up
            self.rotation = 270
        if left and not right:
            self.images = self.img_left
            self.rotation = 180
        if down and not up:
            self.images = self.img_down
            self.rotation = 90
        if right and not left:
            self.images = self.img_right
            self.rotation = 0
        if up or down or left or right:
            if self.initial_shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.initial_shot_timer = shot_timer
                self.game.add_entity(BulletEntity(
                    self.game, self.x, self.y, self.rotation,
                    Category.CHARACTER_BULLET, Category.ENEMY | Category.WALL |
                    Category.CORPSE))

        # check for collision with door object
        obj_layer = self.game.map.get_layer_by_name('object layer')
        for obj in obj_layer:
            if obj.type == 'door':
                # if char.pos is inside the object box:
                if obj.x < self.x < obj.x + obj.width:
                    if obj.y < self.y < obj.y + obj.height:
                        self.x = obj.target_x
                        self.y = obj.target_y
                        self.game.load(obj.target_map)
                        break

    def render(self, surface, r_scale):
        self.particle_effect.render(surface, r_scale)

        # add char image:
        img = self.images[self.img_index]
        width, height = img.get_size()[0], img.get_size()[1]
        r_size = (int(width * r_scale[0]), int(height * r_scale[1]))
        img = pygame.transform.smoothscale(img, r_size)
        r_position = (int(((self.x - width / 2) * r_scale[0])),
                      int((self.y - height / 2) * r_scale[1]))

        if self.particle_effect is not None:
            self.particle_effect.render(surface, r_scale)

        # add surface:
        surface.blit(img, r_position)
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
