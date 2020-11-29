import pygame


class Entity:
    def __init__(self, game):

        # properties:
        self.game = game
        self.marked_for_destroy = False
        self.rotation = 0.0
        self.x = 0
        self.y = 0

        # collisions:
        self.collision_group = 0  # 0 is default
        self.solid = False  # for collisions
        self.solid_collision_box = pygame.Rect(0, 0, 0, 0)
        self.trigger = False
        self.trigger_collision_box = pygame.Rect(0, 0, 0, 0)

    def destroy(self):
        pass

    def update(self, delta_time):
        pass

    def render(self, surface, app, scale):
        if self.game.debugging:
            if self.solid:
                pygame.draw.rect(surface, (255, 255, 255),
                                 (int(self.x + self.solid_collision_box.x),
                                  int(self.y + self.solid_collision_box.y),
                                  self.solid_collision_box.width,
                                  self.solid_collision_box.height), 1)
            if self.trigger:
                pygame.draw.rect(surface, (0, 0, 0),
                                 (int(self.x + self.trigger_collision_box.x),
                                  int(self.y + self.trigger_collision_box.y),
                                  self.trigger_collision_box.width,
                                  self.trigger_collision_box.height), 1)

    def trigger_collision_reaction(self, entity):
        pass
