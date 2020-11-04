from maze.game.entities.bullet_entity import BulletEntity
from maze.game.entities.entity import Entity
from pygame import mixer
import pygame


class CharacterEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.sprites = [pygame.image.load("data/images/character1.png"),
                        pygame.image.load("data/images/character2.png"),
                        pygame.image.load("data/images/character3.png"),
                        pygame.image.load("data/images/character4.png")]
        self.animation_length = 0.12  # controls speed of sprite animation
        self.shooting_timer = 0.2  # prevents the bullets from rapid firing
        self.sprite_index = 0  # needed to iterate through the list of sprites
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
            self.y -= sprite_speed * delta_time
            self.rotation = 0
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.x -= sprite_speed * delta_time
            self.rotation = 90
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.y += sprite_speed * delta_time
            self.rotation = 180
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.x += sprite_speed * delta_time
            self.rotation = 270

        # shooting: (maybe put the repeating code inside a method?)
        bullet_sound = mixer.Sound('data/sounds/laser.wav')
        self.shooting_timer -= delta_time
        shot_speed = 0.2
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.rotation = 0
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                bullet_sound.play()
                self.shooting_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x,
                                                  self.y - 100, self.rotation))
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.rotation = 90
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                bullet_sound.play()
                self.shooting_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x - 100,
                                                  self.y, self.rotation))
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.rotation = 180
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                bullet_sound.play()
                self.shooting_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x,
                                                  self.y + 100, self.rotation))
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.rotation = 270
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                bullet_sound.play()
                self.shooting_timer = shot_speed
                self.game.add_entity(BulletEntity(self.game, self.x + 100,
                                                  self.y, self.rotation))

    def render(self, surface):
        sprite = pygame.transform.rotate(self.sprites[self.sprite_index],
                                         self.rotation)
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        surface.blit(sprite, (int(self.x - width / 2),
                              int(self.y - height / 2)))
