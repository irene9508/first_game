import pygame
from pytmx.util_pygame import load_pygame
from math import sqrt
from operator import attrgetter


class Node:
    def __init__(self, parent, position):
        self.g = 0  # start to node
        self.h = 0  # node to end
        self.f = 0  # start to end

        self.parent = parent
        self.pos = position  # tile index


class Game:
    def __init__(self):
        self.background = pygame.image.load("data/images/bg.jpg").convert()
        self.debugging = False
        self.entities = []
        self.entity_queue = []
        self.map = None

    def find_path(self, startxy, endxy):  # params are tuple of entity position

        opened = []
        closed = []
        existing = {}  # use "x_y" as key
        tile_width = self.map.tilewidth
        tile_height = self.map.tileheight

        # create start and end node:
        start = Node(None, (int(startxy[0] / tile_width),
                            int(startxy[1] / tile_height)))
        end = Node(None, (int(endxy[0] / tile_width),
                          int(endxy[1] / tile_height)))
        existing[str(start.pos[0]) + "_" + str(start.pos[1])] = start
        existing[str(end.pos[0]) + "_" + str(end.pos[1])] = end
        opened.append(start)

        while opened:
            # create current node (sort by f then by h):
            current = min(opened, key=attrgetter('f', 'h'))
            opened.remove(current)
            closed.append(current)

            if current == end:
                path = []
                current_node = current
                while current_node is not None:
                    path.append(current_node.pos)
                    current_node = current_node.parent
                return path[::-1]  # return reversed path

            # for every adjacent tile:
            for adj_x in range(current.pos[0] - 1, current.pos[0] + 2):
                for adj_y in range(current.pos[1] - 1, current.pos[1] + 2):
                    if 0 <= adj_x < self.map.width and 0 <= adj_y < self.map.height:

                        # check if their node exists:
                        adj = None
                        key = str(adj_x) + "_" + str(adj_y)
                        if key not in existing:
                            adj = Node(current, (adj_x, adj_y))
                            existing[key] = adj
                        else:
                            adj = existing[key]

                        # check if we can skip the updating part below:
                        tile_info = self.map.get_tile_properties(adj_x, adj_y, 0)
                        if tile_info['type'] == 'wall' or adj in closed:
                            continue

                        # update some parameters and lists:
                        extra_g = sqrt(abs(current.pos[0] - adj.pos[0]) ** 2 +
                                       abs(current.pos[1] - adj.pos[1]) ** 2)
                        new_g = current.g + extra_g
                        if new_g < adj.g or adj not in opened:
                            adj.g = new_g
                            adj.h = sqrt(abs(adj.pos[0] - end.pos[0]) ** 2 +
                                         abs(adj.pos[1] - end.pos[1]) ** 2)
                            adj.f = adj.g + adj.h
                            adj.parent = current

                            if adj not in opened:
                                opened.append(adj)

        # if loop is exited and no path has been found: return None:
        return None

    def add_entity(self, entity):
        self.entity_queue.append(entity)

    def find_entity_collisions(self, entity1, entity2, coll_box1, coll_box2):

        # define collision box position relative to the screen:
        box1 = pygame.Rect(entity1.x + coll_box1.x, entity1.y + coll_box1.y,
                           coll_box1.width, coll_box1.height)
        box2 = pygame.Rect(entity2.x + coll_box2.x, entity2.y + coll_box2.y,
                           coll_box2.width, coll_box2.height)

        # calculate differences in position:
        diff1 = box1.left - box2.right
        diff2 = box2.left - box1.right
        diff3 = box1.top - box2.bottom
        diff4 = box2.top - box1.bottom

        if diff1 < 0 and diff2 < 0 and diff3 < 0 and diff4 < 0:
            # solve for entities bumping into each other:
            if entity1.solid and entity2.solid:
                self.solve_solid_collision(entity1, entity2,
                                           diff1, diff2, diff3, diff4)

            # trigger a reaction:
            if entity1.collision_group != 0 and entity2.collision_group != 0:
                if entity1.collision_group != entity2.collision_group:
                    if entity1.trigger and entity2.trigger:
                        entity1.trigger_collision_reaction(entity2)
                        entity2.trigger_collision_reaction(entity1)

    def find_neighbouring_walls(self, entity, coll_box_entity):
        entity_tile_index_x = int(entity.x / 80)
        entity_tile_index_y = int(entity.y / 80)

        for x in range(entity_tile_index_x - 1, entity_tile_index_x + 2):
            for y in range(entity_tile_index_y - 1, entity_tile_index_y + 2):
                if 0 <= x < self.map.width and 0 <= y < self.map.height:
                    tile_properties = self.map.get_tile_properties(x, y, 0)
                    if tile_properties['type'] == 'wall':
                        width = int(tile_properties['width'])
                        height = int(tile_properties['height'])
                        coll_box_tile = pygame.Rect(x * width, y * height,
                                                    width, height)
                        self.find_wall_collisions(coll_box_entity,
                                                  coll_box_tile, entity)

    def find_wall_collisions(self, coll_box_entity, tile_box, entity):
        entity_box = pygame.Rect(entity.x + coll_box_entity.x,
                                 entity.y + coll_box_entity.y,
                                 coll_box_entity.width,
                                 coll_box_entity.height)

        diff1 = entity_box.left - tile_box.right
        diff2 = tile_box.left - entity_box.right
        diff3 = entity_box.top - tile_box.bottom
        diff4 = tile_box.top - entity_box.bottom

        if diff1 < 0 and diff2 < 0 and diff3 < 0 and diff4 < 0:
            self.solve_wall_collision(entity, diff1, diff2, diff3, diff4)

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
        # self.map = load_pygame('data/Tiled/trial_room.tmx')
        self.map = load_pygame('data/Tiled/room_with_corridors.tmx')

    def render(self, surface):
        # background:
        # surface.blit(self.background, [0, 0])  # -70fps when active

        # tiles:
        for layer in self.map.layers:
            for x, y, image in layer.tiles():
                surface.blit(image, (self.map.tilewidth * x,
                                     self.map.tileheight * y))

        # isinstance(layer, TiledTileLayer) is needed here later

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
                                                entity1.solid_collision_box,
                                                entity2.solid_collision_box)
                if entity1.trigger and entity2.trigger:
                    self.find_entity_collisions(entity1, entity2,
                                                entity1.trigger_collision_box,
                                                entity2.trigger_collision_box)

        # activate check for collisions between entities and walls:
        for entity in self.entities:
            if entity.solid:
                self.find_neighbouring_walls(entity, entity.solid_collision_box)

        self.initialize_entities()
