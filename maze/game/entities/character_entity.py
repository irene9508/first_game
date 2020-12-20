import pygame
from Box2D import b2FixtureDef, b2CircleShape
from pygame import mixer

from maze.game.entities.bullet_entity import BulletEntity
from maze.game.entities.entity import Entity


class CharacterEntity(Entity):  # 109x93
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
        self.sprites_index = 0  # needed to iterate through the list of sprites
        self.sprites = self.img_down
        self.animation_length = 0.12  # controls speed of sprite animation

        # collisions:
        self.body = self.game.world.CreateDynamicBody(
            position=(self.x * self.game.physics_scale,
                      self.y * self.game.physics_scale),
            userData=self)
        fixt_def = b2FixtureDef(
            shape=b2CircleShape(radius=0.4),
            friction=0.2,
            density=1.0)
        fixt_def.filter.groupIndex = -1
        # noinspection PyUnusedLocal
        fixture = self.body.CreateFixture(fixt_def)

        # properties:
        self.x = 280
        self.y = 300
        self.velocity = [0, 0]

        # other:
        self.shot_timer = 0.2  # prevents the bullets from rapid firing
        self.shot_sound = mixer.Sound('data/sounds/laser.wav')

    def destroy(self):
        self.game.world.DestroyBody(self.body)

    def update(self, delta_time, surface):
        keys = pygame.key.get_pressed()

        # animating, used in render()
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.sprites_index += 1
            if self.sprites_index == len(self.sprites):
                self.sprites_index = 0
            self.animation_length = 0.12

        # movement:
        sprite_speed = 600
        self.velocity = [0, 0]
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.sprites = self.img_up
            self.velocity[1] = -sprite_speed
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.sprites = self.img_left
            self.velocity[0] = -sprite_speed
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.sprites = self.img_down
            self.velocity[1] = sprite_speed
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.sprites = self.img_right
            self.velocity[0] = sprite_speed

        # shooting:
        self.shot_timer -= delta_time
        shot_speed = 0.2
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.sprites = self.img_up
            self.rotation = 90
            if self.shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.shot_timer = shot_speed
                self.game.add_entity(BulletEntity(
                    self.game, self.x, -1, self.y - 52, self.rotation))
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.sprites = self.img_left
            self.rotation = 180
            if self.shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.shot_timer = shot_speed
                self.game.add_entity(BulletEntity(
                    self.game, self.x - 52, -1, self.y, self.rotation))
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.sprites = self.img_down
            self.rotation = 270
            if self.shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.shot_timer = shot_speed
                self.game.add_entity(BulletEntity(
                    self.game, self.x, -1,self.y + 52, self.rotation))
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.sprites = self.img_right
            self.rotation = 0
            if self.shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.shot_timer = shot_speed
                self.game.add_entity(BulletEntity(
                    self.game, self.x + 52, -1, self.y, self.rotation))

    def render(self, surface, render_scale):
        sprite = self.sprites[self.sprites_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        r_size = (int(width * render_scale[0]), int(height * render_scale[1]))
        sprite = pygame.transform.smoothscale(sprite, r_size)
        r_position = (int(((self.x - width / 2) * render_scale[0])),
                      int((self.y - height / 2) * render_scale[1]))

        surface.blit(sprite, r_position)
        super().render(surface, render_scale)

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
