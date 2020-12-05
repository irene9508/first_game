import pygame


class Entity:
    def __init__(self, game, world):

        # properties:
        self.game = game
        self.marked_for_destroy = False
        self.rotation = 0.0
        self.world = world
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

    def render(self, surface, render_scale):
        if self.game.debugging:
            if self.solid:

            if self.trigger:
                pass

        # for layer in self.map.layers:
        #     for x, y, image in layer.tiles():
        #         tile_properties = self.map.get_tile_properties(x, y, 0)
        #         if tile_properties['type'] == 'wall':
        #             tile_body = self.world.CreateStaticBody(
        #                 position=((
        #                                       x * self.map.tilewidth + 0.5 * self.map.tilewidth) * self.physics_scale,
        #                           (
        #                                       y * self.map.tileheight + 0.5 * self.map.tileheight) * self.physics_scale))
        #             tile_body.CreatePolygonFixture(
        #                 box=(0.5 * self.map.tilewidth * self.physics_scale,
        #                      0.5 * self.map.tileheight * self.physics_scale),
        #                 friction=0.2, density=1.0)

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
