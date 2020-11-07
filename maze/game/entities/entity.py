import pygame


class Entity:
    def __init__(self, game):
        self.marked_for_destroy = False
        self.solid_collision_rect = pygame.Rect(0, 0, 0, 0)  # x, y, width, height
        self.debugging = False
        self.rotation = 0.0
        self.solid = False  # for collisions
        self.game = game
        self.x = 0
        self.y = 0

    def destroy(self):
        pass

    def update(self, delta_time):
        pass

    def render(self, surface):
        if self.debugging:
            if self.solid:
                pygame.draw.rect(surface, (255, 255, 255),
                                 (int(self.x + self.solid_collision_rect.x),
                                  int(self.y + self.solid_collision_rect.y),
                                  self.solid_collision_rect.width,
                                  self.solid_collision_rect.height), 1)
