from maze.game.entities.bullet_entity import BulletEntity
from maze.game.entities.entity import Entity
from pygame import mixer
import pygame


class CharacterEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.sprites_left = [pygame.image.load("data/images/enemy1/e1l1.png"),
                             pygame.image.load("data/images/enemy1/e1l2.png"),
                             pygame.image.load("data/images/enemy1/e1l3.png"),
                             pygame.image.load("data/images/enemy1/e1l4.png")]
        self.sprites_right = [pygame.image.load("data/images/enemy1/e1r1.png"),
                              pygame.image.load("data/images/enemy1/e1r2.png"),
                              pygame.image.load("data/images/enemy1/e1r3.png"),
                              pygame.image.load("data/images/enemy1/e1r4.png")]
        self.sprites_up = [pygame.image.load("data/images/enemy1/e1u1.png"),
                           pygame.image.load("data/images/enemy1/e1u2.png"),
                           pygame.image.load("data/images/enemy1/e1u3.png"),
                           pygame.image.load("data/images/enemy1/e1u4.png")]
        self.sprites_down = [pygame.image.load("data/images/enemy1/e1d1.png"),
                             pygame.image.load("data/images/enemy1/e1d2.png"),
                             pygame.image.load("data/images/enemy1/e1d3.png"),
                             pygame.image.load("data/images/enemy1/e1d4.png")]
        self.solid_collision_rect = pygame.Rect(-100, 20, 200, 80)
        self.collision_rect = pygame.Rect(-100, 20, 200, 80)
        self.animation_length = 0.12  # controls speed of sprite animation
        self.shooting_timer = 0.2  # prevents the bullets from rapid firing
        self.sprite_index = 0  # needed to iterate through the list of sprites
        self.bullet_sound = mixer.Sound('data/sounds/laser.wav')
        self.sprites = self.sprites_down
        self.solid = True
        self.x = 280
        self.y = 300

    def update(self, delta_time):
        keys = pygame.key.get_pressed()

        # animating, used in render()
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.sprite_index += 1
            if self.sprite_index == 4:
                self.sprite_index = 0
            self.animation_length = 0.12

        # moving:
        sprite_speed = 300
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
        self.shooting_timer -= delta_time
        shot_speed = 0.2
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.sprites = self.sprites_up
            self.rotation = 0
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                self.bullet_sound.play()
                self.shooting_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x,
                                                  self.y - 150, self.rotation))
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.sprites = self.sprites_left
            self.rotation = 90
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                self.bullet_sound.play()
                self.shooting_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x - 150,
                                                  self.y, self.rotation))
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.sprites = self.sprites_down
            self.rotation = 180
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                self.bullet_sound.play()
                self.shooting_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x,
                                                  self.y + 150, self.rotation))
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.sprites = self.sprites_right
            self.rotation = 270
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                self.bullet_sound.play()
                self.shooting_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x + 150,
                                                  self.y, self.rotation))

    def render(self, surface):
        sprite = self.sprites[self.sprite_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        surface.blit(sprite, (int(self.x - width/2), int(self.y - height/2)))
        super().render(surface)

        # make enemy class that inherits from parent enemy class
