import pygame
from pygame import mixer

from maze.game.entities.bullet_entity import BulletEntity
from maze.game.entities.entity import Entity


class CharacterEntity(Entity):  # 109x93
    def __init__(self, game):
        super().__init__(game)

        # animation:
        self.sprites_down = [
            pygame.image.load("data/images/enemy1/e1d1.png").convert_alpha()]
        self.sprites_left = [
            pygame.image.load("data/images/enemy1/e1l1.png").convert_alpha()]
        self.sprites_right = [
            pygame.image.load("data/images/enemy1/e1r1.png").convert_alpha()]
        self.sprites_up = [
            pygame.image.load("data/images/enemy1/e1u1.png").convert_alpha()]
        self.sprites_index = 0  # needed to iterate through the list of sprites
        self.sprites = self.sprites_down
        self.animation_length = 0.12  # controls speed of sprite animation

        # collisions:
        self.collision_group = 1
        self.collision_box = pygame.Rect(-55, 15, 109, 30)
        self.solid = True
        self.body = self.game.world.CreateDynamicBody(position=(280, 300))
        fixture = self.body.CreateCircleFixture(radius=0.5,
                                                friction=0.2, density=1.0)

        # properties:
        self.x = 280
        self.y = 300

        # other:
        self.shot_timer = 0.2  # prevents the bullets from rapid firing
        self.shot_sound = mixer.Sound('data/sounds/laser.wav')

    def destroy(self):
        self.game.world.DestroyBody(self.body)

    def update(self, delta_time):
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
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.sprites = self.sprites_up
            self.y -= sprite_speed * delta_time
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.sprites = self.sprites_left
            self.x -= sprite_speed * delta_time
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.sprites = self.sprites_down
            self.y += sprite_speed * delta_time
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.sprites = self.sprites_right
            self.x += sprite_speed * delta_time

        # shooting:
        self.shot_timer -= delta_time
        shot_speed = 0.2
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.sprites = self.sprites_up
            self.rotation = 0
            if self.shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.shot_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x, 1,
                                                  self.y - 52, self.rotation))
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.sprites = self.sprites_left
            self.rotation = 90
            if self.shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.shot_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x - 52, 1,
                                                  self.y, self.rotation))
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.sprites = self.sprites_down
            self.rotation = 180
            if self.shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.shot_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x, 1,
                                                  self.y + 52, self.rotation))
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.sprites = self.sprites_right
            self.rotation = 270
            if self.shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.shot_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x + 52, 1,
                                                  self.y, self.rotation))

    def render(self, surface, render_scale):
        sprite = self.sprites[self.sprites_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        sprite = pygame.transform.smoothscale(
            sprite, (int(width * render_scale[0]), int(height * render_scale[1])))
        surface.blit(sprite, (int(((self.x - width / 2) * render_scale[0])),
                              int((self.y - height / 2) * render_scale[1])))
        super().render(surface, render_scale)

    def synchronize_body(self):  # entity gives new info to body
        self.body.position = (self.x * self.game.physics_scale,
                              self.y * self.game.physics_scale)

    def synchronize_entity(self):  # body gives new info to entity
        self.x = self.body.position[0] / self.game.physics_scale
        self.y = self.body.position[1] / self.game.physics_scale
