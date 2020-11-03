from maze.game.entities.entity import Entity
from maze.game.entities.bullet_entity import BulletEntity
import pygame
from pygame import mixer


class CharacterEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.characters = [pygame.image.load("data/images/character1.png"),
                           pygame.image.load("data/images/character2.png"),
                           pygame.image.load("data/images/character3.png"),
                           pygame.image.load("data/images/character4.png")]
        self.animation_length = 0.1
        self.characters_index = 0
        self.shooting_timer = 0.2
        self.x = 280
        self.y = 300

    def update(self, delta_time):
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.characters_index += 1
            if self.characters_index == 4:
                self.characters_index = 0
            self.animation_length = 0.1

        keys = pygame.key.get_pressed()
        character_speed = 300
        shot_speed = 0.2

        # moving:
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.y -= character_speed * delta_time
            self.rotation = 0
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.x -= character_speed * delta_time
            self.rotation = 90
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.y += character_speed * delta_time
            self.rotation = 180
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.x += character_speed * delta_time
            self.rotation = 270

        # shooting:
        self.shooting_timer -= delta_time
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.rotation = 0
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                bullet_sound = mixer.Sound('data/sounds/laser.wav')
                bullet_sound.play()
                self.game.add_entity(BulletEntity(self.game, self.x,
                                                  self.y - 100, self.rotation))
                self.shooting_timer = shot_speed
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.rotation = 90
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                bullet_sound = mixer.Sound('data/sounds/laser.wav')
                bullet_sound.play()
                self.game.add_entity(BulletEntity(self.game, self.x - 100,
                                                  self.y, self.rotation))
                self.shooting_timer = shot_speed
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.rotation = 180
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                bullet_sound = mixer.Sound('data/sounds/laser.wav')
                bullet_sound.play()
                self.game.add_entity(BulletEntity(self.game, self.x,
                                                  self.y + 100, self.rotation))
                self.shooting_timer = shot_speed
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.rotation = 270
            if self.shooting_timer <= 0:
                pygame.mixer.stop()
                bullet_sound = mixer.Sound('data/sounds/laser.wav')
                bullet_sound.play()
                self.game.add_entity(BulletEntity(self.game, self.x + 100,
                                                  self.y, self.rotation))
                self.shooting_timer = shot_speed

    def render(self, surface):
        char = pygame.transform.rotate(self.characters[self.characters_index],
                                       self.rotation)
        width, height = char.get_size()[0], char.get_size()[1]
        surface.blit(char, (int(self.x - width / 2),
                            int(self.y - height / 2)))
