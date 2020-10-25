from maze.game.entities.entity import Entity
import pygame


class CharacterEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.image.load("data/images/character1.png")

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]) \
                or (keys[pygame.K_a] and not keys[pygame.K_d]):
            self.x -= 1.0
        if (keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]) \
                or (keys[pygame.K_d] and not keys[pygame.K_a]):
            self.x += 1.0
        if (keys[pygame.K_UP] and not keys[pygame.K_DOWN]) \
                or (keys[pygame.K_w] and not keys[pygame.K_s]):
            self.y -= 1.0
        if (keys[pygame.K_DOWN] and not keys[pygame.K_UP]) \
                or (keys[pygame.K_s] and not keys[pygame.K_w]):
            self.y += 1.0

    def render(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))
