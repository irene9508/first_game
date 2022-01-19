import pygame

from pytmx.util_pygame import load_pygame
from math import ceil
from Box2D import *  # pip install Box2D /or/ box2d-py

from maze.game.entities.enemy_entity_arnt import EnemyEntityArnt
from maze.game.entities.enemy_entity_blob import EnemyEntityBlob
from maze.game.room_change_behavior import RoomChangeBehavior
from maze.game.my_contact_listener import MyContactListener
from maze.game.collision_masks import Category
from maze.game.my_draw import MyDraw


class Node:
    def __init__(self, parent, tile_index_position):
        self.g = 0  # start to node
        self.h = 0  # node to end
        self.f = 0  # start to end

        self.parent = parent
        self.xy = tile_index_position


class Game:
    def __init__(self, app):
        self.background = pygame.image.load("data/images/bg2.jpg").convert()
        self.debugging = False
        self.entities = []
        self.entity_queue = []
        self.map = None
        self.room = None
        self.rooms = []

        # collisions:
        self.world = b2World(gravity=None, contactListener=MyContactListener())
        self.physics_scale = 1 / 80
        self.world.renderer = MyDraw(app, self.physics_scale)
        self.world.renderer.flags = dict(drawShapes=True)

        # particles:
        # self.particle_effect = ParticleEffect(self)

    def add_entity(self, entity):
        self.entity_queue.append(entity)

    def get_entity_of_category(self, category):
        for entity in self.entities:
            if isinstance(entity, category):
                return entity
        return None

    def initialize_entities(self):
        # remove dead entities:
        new_entities = []
        for entity in self.entities:
            if entity.marked_for_destroy:
                entity.destroy()
            else:
                new_entities.append(entity)
        self.entities = new_entities

        # add queued entities:
        self.entities.extend(self.entity_queue)
        self.entity_queue.clear()

    def load(self, room):
        self.room = room
        self.on_room_exit()
        self.map = load_pygame(room)

        # if room is new, create enemies:
        if room not in self.rooms:
            obj_layer = self.map.get_layer_by_name('object layer')
            for obj in obj_layer:
                if obj.type == 'enemy_blob':
                    self.add_entity(EnemyEntityBlob(self, obj.x, obj.y))
                elif obj.type == 'enemy_arnt':
                    self.add_entity(EnemyEntityArnt(self, obj.x, obj.y))

        # if room is not new, activate its entities:
        if room in self.rooms:
            for entity in self.entities:
                if entity.room == room and not entity.active:
                    entity.activate()

        # create bodies and fixtures for walls:
        tile_layer = self.map.get_layer_by_name('tile layer')
        for x, y, image in tile_layer.tiles():
            tile = self.map.get_tile_properties(x, y, 0)
            if tile['type'] == 'wall':
                # set xy as middle of tile
                x_pos = x * self.map.tilewidth + 0.5 * self.map.tilewidth
                y_pos = y * self.map.tileheight + 0.5 * self.map.tileheight
                tile_body = self.world.CreateStaticBody(
                    position=(x_pos * self.physics_scale,
                              y_pos * self.physics_scale))
                fixt_def = b2FixtureDef(
                    shape=b2PolygonShape(
                        box=(0.5 * self.map.tilewidth * self.physics_scale,
                             0.5 * self.map.tileheight * self.physics_scale)),
                    categoryBits=Category.WALL)
                # noinspection PyUnusedLocal
                fixture = tile_body.CreateFixture(fixt_def)

        if room not in self.rooms:
            self.rooms.append(room)

    def on_room_exit(self):
        # destroy bullets, deactivate still living enemies:
        for entity in self.entities:  # todo: reset to original position? have enemy follow, or reset pos, or close off room until all enemies are dead. keep reference to body for later, then destroy
            if entity.room_change_behavior == RoomChangeBehavior.destroy:
                entity.marked_for_destroy = True
            elif entity.room_change_behavior == RoomChangeBehavior.deactivate:
                entity.deactivate()

        # destroy bodies:
        for body in self.world.bodies:
            if body.userData is None or body.userData.room_change_behavior \
                    == RoomChangeBehavior.deactivate:
                self.world.DestroyBody(body)

    def render(self, surface, r_scale):

        # tiles:
        tile_layer = self.map.get_layer_by_name('tile layer')
        for x, y, image in tile_layer.tiles():
            width = ceil(image.get_size()[0] * r_scale[0])
            height = ceil(image.get_size()[1] * r_scale[1])
            image = pygame.transform.smoothscale(image, (width, height))
            x_pos = int(self.map.tilewidth * x * r_scale[0])
            y_pos = int(self.map.tileheight * y * r_scale[1])
            surface.blit(image, (x_pos, y_pos))

        # entities:
        self.entities.sort(key=lambda e: e.y)
        for entity in self.entities:
            if entity.active:
                entity.render(surface, r_scale)

        # debug data:
        if self.debugging:
            self.world.DrawDebugData()

    def show_debug_info(self):
        self.debugging = not self.debugging

    def update(self, delta_time):
        for entity in self.entities:
            if entity.active:
                entity.update(delta_time)

        for entity in self.entities:
            if entity.active:
                entity.synchronize_body()

        self.world.Step(delta_time, 6, 2)

        for entity in self.entities:
            if entity.active:
                entity.synchronize_entity()

        self.initialize_entities()
