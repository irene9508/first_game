from maze.game.entities.entity import Entity
from maze.game.entities.bullet_entity import BulletEntity
import pygame
from pygame import mixer

class CharacterEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.character = pygame.image.load("data/images/character.png")
        self.x = 280
        self.y = 300

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        speed = 400

        # moving:
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.y -= speed * delta_time
            self.rotation = 0
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.x -= speed * delta_time
            self.rotation = 90
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.y += speed * delta_time
            self.rotation = 180
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.x += speed * delta_time
            self.rotation = 270

        # shooting:
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.rotation = 0
            pygame.mixer.stop()
            bullet_sound = mixer.Sound('data/sounds/laser.wav')
            bullet_sound.play()
            self.game.add_entity(BulletEntity(self.game, self.x, self.y,
                                              self.rotation))
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.rotation = 90
            pygame.mixer.stop()
            bullet_sound = mixer.Sound('data/sounds/laser.wav')
            bullet_sound.play()
            self.game.add_entity(BulletEntity(self.game, self.x, self.y,
                                              self.rotation))
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.rotation = 180
            pygame.mixer.stop()
            bullet_sound = mixer.Sound('data/sounds/laser.wav')
            bullet_sound.play()
            self.game.add_entity(BulletEntity(self.game, self.x, self.y,
                                              self.rotation))
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.rotation = 270
            pygame.mixer.stop()
            bullet_sound = mixer.Sound('data/sounds/laser.wav')
            bullet_sound.play()
            self.game.add_entity(BulletEntity(self.game, self.x, self.y,
                                              self.rotation))

    def render(self, surface):
        character = pygame.transform.rotate(self.character, self.rotation)
        width = character.get_size()[0]
        height = character.get_size()[1]
        surface.blit(character, (int(self.x - width / 2),
                                 int(self.y - height / 2)))
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, 2, 2))
