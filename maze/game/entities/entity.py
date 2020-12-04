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
        self.collision_box = pygame.Rect(0, 0, 0, 0)
        self.trigger = False
        self.hitbox = pygame.Rect(0, 0, 0, 0)

    def destroy(self):
        pass

    def update(self, delta_time):
        pass

    def render(self, surface, scale):
        pass
        # if self.game.debugging:
        #     if self.solid:
        #         self.game.draw.draw_polygon(
        #             (int((self.x + self.collision_box.x) * scale[0]),
        #              int((self.y + self.collision_box.y) * scale[1]),
        #              self.collision_box.width * scale[0],
        #              self.collision_box.height * scale[1]),
        #             surface, (255, 255, 255))
        #     if self.trigger:
        #         self.game.draw.draw_polygon(
        #             (int((self.x + self.hitbox.x) * scale[0]),
        #              int((self.y + self.hitbox.y) * scale[1]),
        #              self.hitbox.width * scale[0],
        #              self.hitbox.height * scale[1]),
        #             surface, (0, 0, 0))

    def synchronize_body(self):
        pass

    def synchronize_entity(self):
        pass

    def trigger_collision_reaction(self, entity):
        pass
