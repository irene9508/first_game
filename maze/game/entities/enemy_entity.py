import pygame

from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.entity import Entity
from math import sqrt


class EnemyEntity(Entity):
    def __init__(self, game):
        super().__init__(game)

        # properties:
        self.health = 0
        self.x = 100
        self.y = 100

        # animation:
        self.current_tile_pos_enemy = None
        self.sprites_left = None
        self.sprites_right = None
        self.sprites_up = None
        self.sprites_down = None
        self.sprites = None
        self.sprites_index = 0  # needed to iterate through the list of sprites
        self.animation_length = 0.12  # controls speed of sprite animation

        # collisions:
        self.collision_group = 2
        self.path = None
        self.solid = True
        self.solid_collision_box = pygame.Rect(0, 0, 0, 0)
        self.trigger = True
        self.trigger_collision_box = pygame.Rect(0, 0, 0, 0)

    def update(self, delta_time):

        # animation, used in render():
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.sprites_index += 1
            if self.sprites_index == len(self.sprites):
                self.sprites_index = 0
            self.animation_length = 0.12

        # health:
        if self.health <= 0:
            self.marked_for_destroy = True

        # movement:
        speed = 150
        character = self.game.get_entity_of_category(CharacterEntity)
        tile_width = self.game.map.tilewidth
        tile_height = self.game.map.tileheight
        p1 = (self.x + self.solid_collision_box.centerx,
              self.y + self.solid_collision_box.centery)
        new_tile_pos_enemy = (int(p1[0] / tile_width), int(p1[1] / tile_height))
        new_tile_pos_char = (character.x + character.solid_collision_box.centery)

        if character is not None:

            if self.current_tile_pos_enemy != new_tile_pos_enemy:
                self.current_tile_pos_enemy = new_tile_pos_enemy

                # find path to character:
                self.path = self.game.find_path(p1,
                    (character.x + character.solid_collision_box.centerx,
                     character.y + character.solid_collision_box.centery))

            # move towards next node:
            p2 = (self.path[1][0] * tile_width + tile_width / 2,
                  self.path[1][1] * tile_height + tile_height / 2)

            vector = (p2[0] - p1[0], p2[1] - p1[1])
            length = sqrt(vector[0] * vector[0] + vector[1] * vector[1])
            v_norm = (vector[0] / length, vector[1] / length)

            movement = (v_norm[0] * speed, v_norm[1] * speed)

            self.x += movement[0] * delta_time
            self.y += movement[1] * delta_time

            # facing towards player:
            if abs(vector[1]) > abs(vector[0]):
                if vector[0] < 0:
                    self.sprites = self.sprites_up
                else:
                    self.sprites = self.sprites_down
            else:
                if vector[1] < 0:
                    self.sprites = self.sprites_right
                else:
                    self.sprites = self.sprites_left

    def render(self, surface):
        sprite = self.sprites[self.sprites_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        surface.blit(sprite, (int(self.x - width/2), int(self.y - height/2)))
        super().render(surface)

        if self.game.debugging and self.path is not None:
            for index in range(len(self.path) - 1):
                pygame.draw.line(surface, (0, 0, 255),
                                 (self.path[index][0] * self.game.map.tilewidth
                                  + self.game.map.tilewidth / 2,
                                  self.path[index][1] * self.game.map.tileheight
                                  + self.game.map.tileheight / 2),
                                 (self.path[index + 1][0]
                                  * self.game.map.tilewidth
                                  + self.game.map.tilewidth / 2,
                                  self.path[index + 1][1]
                                  * self.game.map.tileheight
                                  + self.game.map.tileheight / 2))
