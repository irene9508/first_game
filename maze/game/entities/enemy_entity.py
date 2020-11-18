from maze.game.entities.entity import Entity
from maze.game.entities.character_entity import CharacterEntity
import pygame


class EnemyEntity(Entity):
    def __init__(self, game):
        super().__init__(game)

        # properties:
        self.health = 0
        self.x = 100
        self.y = 100

        # animation:
        self.sprites_left = None
        self.sprites_right = None
        self.sprites_up = None
        self.sprites_down = None
        self.sprites = None
        self.sprites_index = 0  # needed to iterate through the list of sprites
        self.animation_length = 0.12  # controls speed of sprite animation

        # collisions:
        self.collision_group = 2
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
        speed = 50
        character = self.game.get_entity_of_category(CharacterEntity)
        if character is not None:
            self.path = self.game.find_path((self.x + self.solid_collision_box.centerx,
                                        self.y + self.solid_collision_box.centery),
                                       (character.x + character.solid_collision_box.centerx,
                                        character.y + character.solid_collision_box.centery))

            # moving towards next node:
            node_position = (self.path[1][0] * self.game.map.tilewidth + self.game.map.tilewidth / 2,
                             self.path[1][1] * self.game.map.tileheight + self.game.map.tileheight / 2)

            # moving towards player:
            x_distance = self.x + self.solid_collision_box.centerx - node_position[0]
            y_distance = self.y + self.solid_collision_box.centery - node_position[1]
            if abs(y_distance) < 1:
                self.y = node_position[1] - self.solid_collision_box.centery
            if y_distance > 0:
                self.y -= speed * delta_time
            elif y_distance < 0:
                self.y += speed * delta_time
            if abs(x_distance) < 1:
                self.x = node_position[0] - self.solid_collision_box.centerx
            if x_distance < 0:
                self.x += speed * delta_time
            elif x_distance > 0:
                self.x -= speed * delta_time

            # facing towards player
            if abs(y_distance) > abs(x_distance):
                if y_distance < 0:
                    self.sprites = self.sprites_down
                else:
                    self.sprites = self.sprites_up
            else:
                if x_distance < 0:
                    self.sprites = self.sprites_right
                else:
                    self.sprites = self.sprites_left

    def render(self, surface):
        sprite = self.sprites[self.sprites_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        surface.blit(sprite, (int(self.x - width/2), int(self.y - height/2)))
        super().render(surface)

        if self.game.debugging:
            if self.path is not None:
                for index in range(len(self.path) - 1):
                    pygame.draw.line(surface, (0, 0, 255),
                                     (self.path[index][0] * self.game.map.tilewidth + self.game.map.tilewidth / 2,
                                      self.path[index][1] * self.game.map.tileheight + self.game.map.tileheight / 2),
                                     (self.path[index + 1][0] * self.game.map.tilewidth + self.game.map.tilewidth / 2,
                                      self.path[index + 1][1] * self.game.map.tileheight + self.game.map.tileheight / 2))
