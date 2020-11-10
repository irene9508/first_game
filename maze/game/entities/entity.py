import pygame


class Entity:
    def __init__(self, game):
        self.collision_group = 0  # 0 is default
        self.collision_rect_solid = pygame.Rect(0, 0, 0, 0)  # x/y/width/height
        self.collision_rect_trigger = pygame.Rect(0, 0, 0, 0)
        self.game = game
        self.marked_for_destroy = False
        self.rotation = 0.0
        self.solid = False  # for collisions
        self.trigger = False
        self.x = 0
        self.y = 0

    def destroy(self):
        pass

    def update(self, delta_time, screen_width, screen_height):
        pass

    def render(self, surface):
        if self.game.debugging:
            if self.solid:
                pygame.draw.rect(surface, (255, 255, 255),
                                 (int(self.x + self.collision_rect_solid.x),
                                  int(self.y + self.collision_rect_solid.y),
                                  self.collision_rect_solid.width,
                                  self.collision_rect_solid.height), 1)
            if self.trigger:
                pygame.draw.rect(surface, (255, 0, 255),
                                 (int(self.x + self.collision_rect_trigger.x),
                                  int(self.y + self.collision_rect_trigger.y),
                                  self.collision_rect_trigger.width,
                                  self.collision_rect_trigger.height), 1)

    def solve_trigger_collision(self, entity):
        pass
