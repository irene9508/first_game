from math import ceil

import pygame

from maze.game.my_contact_listener import MyContactListener
from maze.game.my_draw import MyDraw
from maze.game.entities.enemy_entity_blob import EnemyEntityBlob
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

    def add_entity(self, entity):
        self.entity_queue.append(entity)

    def destroy_bodies(self):
        for body in self.world.bodies:
            if body.type == b2_staticBody:
                self.world.DestroyBody(body)

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

    def load(self, room):
        self.map = load_pygame(room)

        # create enemies:
        obj_layer = self.map.get_layer_by_name('object layer')
        for obj in obj_layer:
            if obj.type == 'enemy':
                self.add_entity(EnemyEntityBlob(self, obj.x, obj.y))

        # create bodies and fixtures:
        tile_layer = self.map.get_layer_by_name('tile layer')
        for x, y, image in tile_layer.tiles():
            tile_properties = self.map.get_tile_properties(x, y, 0)
            if tile_properties['type'] == 'wall' or tile_properties['type'] == 'door':
                tile_body = self.world.CreateStaticBody(
                    position=((x * self.map.tilewidth +
                               0.5 * self.map.tilewidth) * self.physics_scale,
                              (y * self.map.tileheight +
                               0.5 * self.map.tileheight) * self.physics_scale))
                tile_body.CreatePolygonFixture(
                    box=(0.5 * self.map.tilewidth * self.physics_scale,
                         0.5 * self.map.tileheight * self.physics_scale),
                    friction=0.2, density=1.0)

    def render(self, surface, render_scale):

        # tiles:
        tile_layer = self.map.get_layer_by_name('tile layer')
        for x, y, image in tile_layer.tiles():
            width, height = image.get_size()[0], image.get_size()[1]
            image = pygame.transform.smoothscale(
                image,
                (ceil(width * render_scale[0]), ceil(height * render_scale[1])))
            surface.blit(image, (int(self.map.tilewidth * x * render_scale[0]),
                                 int(self.map.tileheight * y * render_scale[
                                     1])))

        # entities:
        self.entities.sort(key=lambda e: e.y)
        for entity in self.entities:
            entity.render(surface, render_scale)

        if self.debugging:
            self.world.DrawDebugData()

    def show_debug_info(self):
        self.debugging = not self.debugging

    def update(self, delta_time):
        for entity in self.entities:
            entity.update(delta_time)

        for entity in self.entities:
            entity.synchronize_body()

        self.world.Step(delta_time, 6, 2)

        for entity in self.entities:
            entity.synchronize_entity()

        self.initialize_entities()
