import pygame
from pytmx.util_pygame import load_pygame
# from math import floor


class Game:
    def __init__(self):
        self.background = pygame.image.load("data/images/background.jpg").convert()
        self.debugging = False
        self.entities = []
        self.entity_queue = []
        self.map = None

    def add_entity(self, entity):
        self.entity_queue.append(entity)

    def find_entity_collisions(self, entity1, entity2, coll_rect1, coll_rect2):
        # define collision rectangles:
        rect1 = pygame.Rect(entity1.x + coll_rect1.x, entity1.y + coll_rect1.y,
                            coll_rect1.width, coll_rect1.height)
        rect2 = pygame.Rect(entity2.x + coll_rect2.x, entity2.y + coll_rect2.y,
                            coll_rect2.width, coll_rect2.height)

        # calculate differences in position:
        diff1 = rect1.left - rect2.right
        diff2 = rect2.left - rect1.right
        diff3 = rect1.top - rect2.bottom
        diff4 = rect2.top - rect1.bottom

        if diff1 < 0 and diff2 < 0 and diff3 < 0 and diff4 < 0:
            # solve for entities bumping into each other:
            if entity1.solid and entity2.solid:
                self.solve_solid_collision(entity1, entity2, diff1, diff2,
                                           diff3, diff4)
            # trigger a reaction:
            if entity1.collision_group != 0 and entity2.collision_group != 0:
                if entity1.collision_group != entity2.collision_group:
                    if entity1.trigger and entity2.trigger:
                        entity1.trigger_collision_reaction(entity2)
                        entity2.trigger_collision_reaction(entity1)

    def find_neighbouring_walls(self, entity, coll_rect_entity):
        entity_tile_index_x = int(entity.x / 80)
        entity_tile_index_y = int(entity.y / 80)

        for x in range(entity_tile_index_x - 1, entity_tile_index_x + 2):
            for y in range(entity_tile_index_y - 1, entity_tile_index_y + 2):
                if 0 <= x < self.map.width and 0 <= y < self.map.height:
                    tile_properties = self.map.get_tile_properties(x, y, 0)
                    if tile_properties['type'] == 'wall':
                        coll_rect_tile = pygame.Rect(x * int(tile_properties['width']),
                                                     y * int(tile_properties['height']),
                                                     int(tile_properties['width']),
                                                     int(tile_properties['height']))
                        self.find_wall_collisions(coll_rect_entity, coll_rect_tile,
                                                  entity)

    def find_wall_collisions(self, coll_rect_entity, tile_rect, entity):
        entity_rect = pygame.Rect(entity.x + coll_rect_entity.x,
                                  entity.y + coll_rect_entity.y,
                                  coll_rect_entity.width,
                                  coll_rect_entity.height)

        diff1 = entity_rect.left - tile_rect.right
        diff2 = tile_rect.left - entity_rect.right
        diff3 = entity_rect.top - tile_rect.bottom
        diff4 = tile_rect.top - entity_rect.bottom

        if diff1 < 0 and diff2 < 0 and diff3 < 0 and diff4 < 0:
            self.solve_wall_collision(entity, diff1, diff2, diff3, diff4)
        # solve collision between the rect and the entity solid rect

    def get_entity_of_category(self, category):
        for entity in self.entities:
            if isinstance(entity, category):
                return entity
        return None

    def initialize_entities(self):
        # remove dead entities:
        new_entities = []
        for entity in self.entities:
            entity.destroy() if entity.marked_for_destroy \
                else new_entities.append(entity)
        self.entities = new_entities

        # add queued entities:
        self.entities.extend(self.entity_queue)
        self.entity_queue.clear()

    def load(self):
        self.map = load_pygame('data/Tiled/trial_room.tmx')

    def render(self, surface):
        # background:
        surface.blit(self.background, [0, 0])

        # tiles:
        for layer in self.map.layers:
            for x, y, image in layer.tiles():
                surface.blit(image, (self.map.tilewidth * x,
                                     self.map.tileheight * y))
        # isinstance(layer, TiledTileLayer)

        # entities:
        self.entities.sort(key=lambda e: e.y)
        for entity in self.entities:
            entity.render(surface)

    def show_debug_info(self):
        self.debugging = not self.debugging

    @staticmethod
    def solve_solid_collision(entity1, entity2, diff1, diff2, diff3, diff4):
        least_difference = min(abs(diff1), abs(diff2), abs(diff3), abs(diff4))
        if least_difference == abs(diff1):
            entity1.x -= diff1 * 0.5
            entity2.x += diff1 * 0.5
        elif least_difference == abs(diff2):
            entity1.x += diff2 * 0.5
            entity2.x -= diff2 * 0.5
        elif least_difference == abs(diff3):
            entity1.y -= diff3 * 0.5
            entity2.y += diff3 * 0.5
        elif least_difference == abs(diff4):
            entity1.y += diff4 * 0.5
            entity2.y -= diff4 * 0.5

    @staticmethod
    def solve_wall_collision(entity, diff1, diff2, diff3, diff4):
        least_difference = min(abs(diff1), abs(diff2), abs(diff3), abs(diff4))
        if least_difference == abs(diff1):
            entity.x -= diff1
        elif least_difference == abs(diff2):
            entity.x += diff2
        elif least_difference == abs(diff3):
            entity.y -= diff3
        elif least_difference == abs(diff4):
            entity.y += diff4

    def update(self, delta_time):
        for entity in self.entities:
            entity.update(delta_time)

        # activate check for collisions between entities:
        for index1, entity1 in enumerate(self.entities):
            for entity2 in self.entities[index1 + 1:]:
                if entity1.solid and entity2.solid:
                    self.find_entity_collisions(entity1, entity2,
                                                entity1.collision_rect_solid,
                                                entity2.collision_rect_solid)
                if entity1.trigger and entity2.trigger:
                    self.find_entity_collisions(entity1, entity2,
                                                entity1.collision_rect_trigger,
                                                entity2.collision_rect_trigger)

        # activate check for collisions between entities and walls:
        for entity in self.entities:
            if entity.solid:
                self.find_neighbouring_walls(entity, entity.collision_rect_solid)

        self.initialize_entities()
