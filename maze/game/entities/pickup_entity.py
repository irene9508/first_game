from math import sqrt

import pygame
from pygame import image as img
from Box2D import b2FixtureDef, b2CircleShape

from maze.game.collision_masks import Category
from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.entity import Entity


class PickupEntity(Entity):
    def __init__(self, game, x, y):
        super().__init__(game)

        self.velocity = None
        self.x = x
        self.y = y
        self.surface = None
        self.r_scale = None
        self.img = img.load("data/images/star.png").convert_alpha()

        position = (self.x * self.game.physics_scale, self.y * self.game.physics_scale)
        self.body = self.game.world.CreateDynamicBody(position=position, userData=self)
        fixt_def = b2FixtureDef(shape=b2CircleShape(radius=0.1), isSensor=True,
                                categoryBits=Category.PICKUP,
                                maskBits=(Category.ENEMY | Category.CHARACTER |
                                          Category.CHARACTER_BULLET | Category.WALL |
                                          Category.CORPSE))

    def render(self, surface, r_scale):
        self.r_scale, self.surface = r_scale, surface
        width, height = self.img.get_size()[0], self.img.get_size()[1]
        r_size = (int(width * r_scale[0]), int(height * r_scale[1]))
        sprite = pygame.transform.smoothscale(self.img, r_size)
        r_position = (int(((self.x - width / 2) * r_scale[0])),
                      int((self.y - height / 2) * r_scale[1]))

        surface.blit(sprite, r_position)
        super().render(surface, r_scale)

    def update(self, delta_time):
        self.velocity = [0, 0]

        char = self.game.get_entity_of_category(CharacterEntity)
        distance = sqrt((char.x - self.x) ** 2 + (char.y - self.y) ** 2)

        if distance < 80:
            self.img = img.load("data/images/star_near.png").convert_alpha()
        else:
            self.img = img.load("data/images/star.png").convert_alpha()
