from math import sqrt, ceil
from operator import attrgetter

import pygame

from maze.game.my_contact_listener import MyContactListener
from maze.game.my_draw import MyDraw
from pytmx.util_pygame import load_pygame
from Box2D import *  # pip install Box2D


class Node:
    def __init__(self, parent, tile_index_position):
        self.g = 0  # start to node
        self.h = 0  # node to end
        self.f = 0  # start to end

        self.parent = parent
        self.xy = tile_index_position


class Game:
    def __init__(self, app):
        self.background = pygame.image.load("data/images/bg.jpg").convert()
        self.debugging = False
        self.entities = []
        self.entity_queue = []
        self.map = None

        # collisions:
        self.world = b2World(gravity=None, contactListener=MyContactListener())
        self.physics_scale = 1 / 80
        self.world.renderer = MyDraw(app, self.physics_scale)
        self.world.renderer.flags = dict(drawShapes=True)

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
                new_path = []
                checkpoint = path[0]
                new_path.append(checkpoint)
                for index in range(1, len(path) - 1):
                    walkable = self.check_if_walkable(checkpoint,
                                                      path[index + 1])
                    if not walkable:
                        checkpoint = path[index]
                        new_path.append(path[index])
                new_path.append(path[-1])
                return new_path

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
                        tile_info = self.map.get_tile_properties(
                            adj_x, adj_y, 0)
                        if tile_info['type'] == 'wall' or adj in closed:
                            continue

                        # check if diagonal jumps are valid:
                        if adj_x != cur_x and adj_y != cur_y:
                            tile_info1 = self.map.get_tile_properties(
                                cur_x, adj_y, 0)
                            tile_info2 = self.map.get_tile_properties(
                                adj_x,cur_y, 0)
                            if 'wall' in [
                                    tile_info1['type'], tile_info2['type']]:
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

    def check_if_walkable(self, point1, point2):
        tile_width = self.map.tilewidth
        tile_height = self.map.tileheight
        p1 = (point1[0] * tile_width + tile_width / 2,
              point1[1] * tile_height + tile_height / 2)
        p2 = (point2[0] * tile_width + tile_width / 2,
              point2[1] * tile_height + tile_height / 2)
        vector1 = (p2[0] - p1[0], p2[1] - p1[1])
        length1 = sqrt(vector1[0] * vector1[0] + vector1[1] * vector1[1])
        v_norm1 = (vector1[0] / length1, vector1[1] / length1)

        for distance in range(0, int(length1), int(tile_width / 5)):
            x1 = p1[0] + v_norm1[0] * distance
            y1 = p1[1] + v_norm1[1] * distance

            tile_info1 = self.map.get_tile_properties(
                x1 / tile_width, y1 / tile_height, 0)
            tile_info2 = self.map.get_tile_properties(
                x1 / tile_width + 0.5, y1 / tile_height + 0.5, 0)
            tile_info3 = self.map.get_tile_properties(
                x1 / tile_width - 0.5, y1 / tile_height - 0.5, 0)

            if 'wall' in [
                    tile_info1['type'], tile_info2['type'], tile_info3['type']]:
                return False

        # if no wall tile was found, return True:
        return True

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
                self.solve_solid_collision(
                    entity1, entity2, diff1, diff2, diff3, diff4)

            # trigger a reaction:
            if entity1.collision_group != 0 and entity2.collision_group != 0:
                if entity1.collision_group != entity2.collision_group:
                    if entity1.trigger and entity2.trigger:
                        entity1.trigger_collision_reaction(entity2)
                        entity2.trigger_collision_reaction(entity1)

    def find_neighbouring_walls(self, entity, coll_box_entity):
        entity_tile_index_x = int(entity.x / self.map.tilewidth)
        entity_tile_index_y = int(entity.y / self.map.tileheight)

        for x in range(entity_tile_index_x - 1, entity_tile_index_x + 2):
            for y in range(entity_tile_index_y - 1, entity_tile_index_y + 2):
                if 0 <= x < self.map.width and 0 <= y < self.map.height:
                    tile_properties = self.map.get_tile_properties(x, y, 0)
                    if tile_properties['type'] == 'wall':
                        width = int(tile_properties['width'])
                        height = int(tile_properties['height'])
                        coll_box_tile = pygame.Rect(
                            x * width, y * height, width, height)
                        self.find_wall_collisions(
                            coll_box_entity, coll_box_tile, entity)

    def find_wall_collisions(self, coll_box_entity, tile_box, entity):
        entity_box = pygame.Rect(
            entity.x + coll_box_entity.x, entity.y + coll_box_entity.y,
            coll_box_entity.width, coll_box_entity.height)

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

        # create collision boxes:
        tile_layer = self.map.get_layer_by_name('tile layer')
        for x, y, image in tile_layer:
            tile_properties = self.map.get_tile_properties(x, y, 0)
            if tile_properties['type'] == 'wall':
                tile_body = self.world.CreateStaticBody(
                    position=((x * self.map.tilewidth + 0.5 * self.map.tilewidth) * self.physics_scale,
                              (y * self.map.tileheight + 0.5 * self.map.tileheight) * self.physics_scale))
                tile_body.CreatePolygonFixture(
                    box=(0.5 * self.map.tilewidth * self.physics_scale,
                         0.5 * self.map.tileheight * self.physics_scale),
                    friction=0.2, density=1.0)

    def render(self, surface, render_scale):

        # tiles:
        tile_layer = self.map.get_layer_by_name('tile layer')
        for x, y, image in tile_layer:
            width, height = image.get_size()[0], image.get_size()[1]
            image = pygame.transform.smoothscale(
                image, (ceil(width * render_scale[0]), ceil(height * render_scale[1])))
            surface.blit(image, (int(self.map.tilewidth * x * render_scale[0]),
                                 int(self.map.tileheight * y * render_scale[1])))

        # entities:
        self.entities.sort(key=lambda e: e.y)
        for entity in self.entities:
            entity.render(surface, render_scale)

        if self.debugging:
            self.world.DrawDebugData()

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

        # # activate check for collisions between entities:
        # for index1, entity1 in enumerate(self.entities):
        #     for entity2 in self.entities[index1 + 1:]:
        #         if entity1.solid and entity2.solid:
        #             self.find_entity_collisions(entity1, entity2,
        #                                         entity1.collision_box,
        #                                         entity2.collision_box)
        #         if entity1.trigger and entity2.trigger:
        #             self.find_entity_collisions(entity1, entity2,
        #                                         entity1.hitbox,
        #                                         entity2.hitbox)
        #
        # # activate check for collisions between entities and walls:
        # for entity in self.entities:
        #     if entity.solid:
        #         self.find_neighbouring_walls(entity, entity.collision_box)

        for entity in self.entities:
            entity.synchronize_body()

        self.world.Step(delta_time, 6, 2)
        self.world.DrawDebugData()

        for entity in self.entities:
            entity.synchronize_entity()

        self.initialize_entities()
