from maze.game.entities.entity import Entity
from maze.game.entities.bullet_entity import BulletEntity
import pygame


class CharacterEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.image.load("data/images/character6.png")

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.x -= 1.0
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.x += 1.0
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.y -= 1.0
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.y += 1.0
        if keys[pygame.K_UP]:
            self.game.add_entity(BulletEntity(self.game, self.x, self.y))

    def render(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))
