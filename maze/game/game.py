from math import ceil

import pygame

from maze.game.entities.character_entity import CharacterEntity
from maze.game.my_contact_listener import MyContactListener
from maze.game.my_draw import MyDraw
from maze.game.entities.bullet_entity import BulletEntity
from maze.game.entities.enemy_entity import EnemyEntity
from maze.game.entities.enemy_entity_blob import EnemyEntityBlob
from pytmx.util_pygame import load_pygame
from Box2D import *  # pip install Box2D /or/ box2d-py


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
        self.rooms = []

        # collisions:
        self.world = b2World(gravity=None, contactListener=MyContactListener())
        self.physics_scale = 1 / 80
        self.world.renderer = MyDraw(app, self.physics_scale)
        self.world.renderer.flags = dict(drawShapes=True)

    def add_entity(self, entity):
        self.entity_queue.append(entity)

    def destroy_or_deactivate_old_bodies_or_entities(self):
        # destroy bullets, deactivate still living enemies:
        for entity in self.entities:
            if isinstance(entity, BulletEntity):
                entity.marked_for_destroy = True
            if isinstance(entity, EnemyEntity):
                entity.active = False

        # destroy bodies:
        for body in self.world.bodies:
            if not isinstance(body.userData, CharacterEntity):
                self.world.DestroyBody(body)
            # body.linearVelocity = (0, (body)
# I am trying to destroy bodies when switching screens, and recreate them when
# switching back to the first screen. Those actions need to happen in the
# EnemyEntity class; it has all the references that are needed to get it
# working. There already is a method called DESTROY that destroys the bodies. I
# think I just need to call that method in game.destroy_or_deactivate.

# I'm not sure yet how to create the new body. I am keeping the enemy instance,
# and creating a new body for it.

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
        self.destroy_or_deactivate_old_bodies_or_entities()
        self.map = load_pygame(room)

        # if room has not been visited before, create enemies:
        if room not in self.rooms:
            obj_layer = self.map.get_layer_by_name('object layer')
            for obj in obj_layer:
                if obj.type == 'enemy':
                    self.add_entity(EnemyEntityBlob(self, obj.x, obj.y, room))

        # if room was visited before, activate entities belonging to the room,
        # and activate collision detection for now active entities:
        if room in self.rooms:
            for entity in self.entities:
                if not isinstance(entity, CharacterEntity):
                    if not isinstance(entity, BulletEntity):
                        if entity.room == room and not entity.active:
                            entity.active = True
                    if entity.active:
                        entity.create_new_body()
            for body in self.world.bodies:
                if not isinstance(body.userData, CharacterEntity):
                    if body.userData.active:
                        for fixture in body.fixtures:
                            fixture.filterData.maskBits = 65535

        # create bodies and fixtures for walls:
        tile_layer = self.map.get_layer_by_name('tile layer')
        for x, y, image in tile_layer.tiles():
            tile = self.map.get_tile_properties(x, y, 0)
            if tile['type'] == 'wall' or tile['type'] == 'door':
                x_pos = x * self.map.tilewidth + 0.5 * self.map.tilewidth
                y_pos = y * self.map.tileheight + 0.5 * self.map.tileheight
                tile_body = self.world.CreateStaticBody(
                    position=(x_pos * self.physics_scale,
                              y_pos * self.physics_scale))
                tile_body.CreatePolygonFixture(
                    box=(0.5 * self.map.tilewidth * self.physics_scale,
                         0.5 * self.map.tileheight * self.physics_scale),
                    friction=0.2, density=1.0
                )

        if room not in self.rooms:
            self.rooms.append(room)

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
