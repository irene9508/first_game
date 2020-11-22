from math import sqrt
from operator import attrgetter

import pygame
from pytmx.util_pygame import load_pygame


class Node:
    def __init__(self, parent, position):
        self.g = 0  # start to node
        self.h = 0  # node to end
        self.f = 0  # start to end

        self.parent = parent
        self.xy = position  # tile index


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
        tile_width, tile_height = self.map.tilewidth, self.map.tileheight
        map_width, map_height = self.map.width, self.map.height

        # create start and end node:
        start = Node(None, (int(startxy[0] / tile_width),
                            int(startxy[1] / tile_height)))
        end = Node(None, (int(endxy[0] / tile_width),
                          int(endxy[1] / tile_height)))
        existing[str(start.xy[0]) + "_" + str(start.xy[1])] = start
        existing[str(end.xy[0]) + "_" + str(end.xy[1])] = end
        opened.append(start)

        while opened:
            # create current node (sort by f then by h):
            current = min(opened, key=attrgetter('f', 'h'))
            opened.remove(current)
            closed.append(current)

            # make path:
            if current == end:
                path = []
                current_node = current
                while current_node is not None:
                    path.append(current_node.xy)
                    current_node = current_node.parent
                path = path[::-1]

                # skip unnecessary nodes:

                # start at first node:
                checkpoint = path[0]
                # for every following node:
                for index, point in enumerate(path[1:], start=1):
                    if index < len(path) - 1:
                        # check if path from checkpoint to point is walkable:
                        walkable = self.check_if_walkable(checkpoint, point)
                        # if path from eg. point 0 to point 2 is walkable:
                        if walkable and index < len(path) - 1:
                            # temporarily store point 1:
                            temp = path[index - 1]
                            # remove point 1 from list:
                            path.remove(temp)
                        # if path is not walkable:
                        else:
                            # make point 1 the checkpoint:
                            checkpoint = path[index]
                return path

            cur_x, cur_y = current.xy[0], current.xy[1]

            # for every adjacent tile:
            for adj_x in range(cur_x - 1, cur_x + 2):
                for adj_y in range(cur_y - 1, cur_y + 2):
                    if 0 <= adj_x < map_width and 0 <= adj_y < map_height:

                        # check if the node exists:
                        adj = None
                        key = str(adj_x) + "_" + str(adj_y)
                        if key not in existing:
                            adj = Node(current, (adj_x, adj_y))
                            existing[key] = adj
                        else:
                            adj = existing.get(key)

                        # check if the node is walkable:
                        tile_info = self.map.get_tile_properties(adj_x, adj_y,
                                                                 0)
                        if tile_info['type'] == 'wall' or adj in closed:
                            continue

                        # check if diagonal jumps are valid:
                        if adj_x != cur_x and adj_y != cur_y:
                            tile_info1 = self.map.get_tile_properties(cur_x,
                                                                      adj_y, 0)
                            tile_info2 = self.map.get_tile_properties(adj_x,
                                                                      cur_y, 0)
                            if tile_info1['type'] == 'wall' \
                                    or tile_info2['type'] == 'wall':
                                continue

                        # update some parameters and lists:
                        extra_g = sqrt(abs(current.xy[0] - adj.xy[0]) ** 2 +
                                       abs(current.xy[1] - adj.xy[1]) ** 2)
                        new_g = current.g + extra_g
                        if new_g < adj.g or adj not in opened:
                            adj.g = new_g
                            adj.h = sqrt(abs(adj.xy[0] - end.xy[0]) ** 2 +
                                         abs(adj.xy[1] - end.xy[1]) ** 2)
                            adj.f = adj.g + adj.h
                            adj.parent = current

                            if adj not in opened:
                                opened.append(adj)

        # if no path:
        return None

    def check_if_walkable(self, checkpoint, point):
        x1, y1 = checkpoint[0], checkpoint[1]
        x2, y2 = point[0], point[1]
        slope = (y1 - y2) / (x1 - x2)
        y_intercept = (x1 * y2 - x2 * y1) / (x1 - x2)

        # if slope is more horizontal, or exactly diagonal:
        if -45 <= slope <= 45:
            # make sure the for-loop knows whether to add or subtract interval:
            if slope < 0:
                sign = -1
            else:
                sign = 1
            # for every xth coordinate on x-axis:
            for x in range(x1, x2, sign * int(self.map.tilewidth / 5)):
                # get the corresponding y coordinate:
                y = int(slope * x + y_intercept)
                # get the tile info for these coordinates:
                tile_info = self.map.get_tile_properties(x, y, 0)
                # if tile is wall, path is not walkable, return False:
                if tile_info['type'] == 'wall':
                    return False
                # else, continue checking the next point in the path:
                else:
                    continue
            # if no wall tile was found, return True:
            return True

        # if slope is more vertical:
        if slope < -45 or slope > 45:
            # make sure the for-loop knows whether to add or subtract interval:
            if slope < 0:
                sign = -1
            else:
                sign = 1
            # for every xth coordinate on y-axis:
            for y in range(y1, y2, sign * (self.map.tilewidth / 5)):
                # get the corresponding x coordinate:
                x = (y - y_intercept) / slope
                # get the tile info for these coordinates:
                tile_info = self.map.get_tile_properties(x, y, 0)
                # if tile is wall, path is not walkable, return False:
                if tile_info['type'] == 'wall':
                    return False
                # else, continue checking the next point in the path:
                else:
                    continue
            # if no wall tile was found, return True:
            return True


        # find the line from checkpoint to current_point
        # find out if the line is more horizontal or more vertical
        # if more horizontal: use x-axis; if more vertical: use y-axis
        # if exactly diagonal, it doesn't matter: use x-axis
        # every so many coordinates (1/5th of tile width), get x/y coordinates
        # use the coordinates to get tile info, and check if tile is wall
        # if not: check next point in path, until end is reached. Return True.
        # as soon as a tile is a wall: return False

        # The algorithm makes use of a function Walkable(pointA, pointB),
        # which samples points along a line from point A to point B at a
        # certain granularity (typically we use one-fifth of a tile width),
        # checking at each point whether the unit overlaps any neighboring
        # blocked tile. (Using the width of the unit, it checks the four
        # points in a diamond pattern around the unit's center.) The function
        # returns true if it encounters no blocked tiles and false otherwise.
        # See Figure 3 for an illustration, and Listing 1 for pseudocode.

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
