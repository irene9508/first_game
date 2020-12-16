import pygame
from Box2D import b2FixtureDef, b2CircleShape, b2RayCastCallback

from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.entity import Entity
from maze.game.path_finder import PathFinder
from math import sqrt


class RayCastCallback(b2RayCastCallback):

    def __init__(self, **kwargs):
        b2RayCastCallback.__init__(self)
        self.fraction = None

    def ReportFixture(self, fixture, point, normal, fraction):
        self.fraction = fraction
        return fraction


class EnemyEntity(Entity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game)

        # properties:
        self.health = 0
        self.x = spawn_x
        self.y = spawn_y
        self.velocity = [0, 0]

        # animation:
        self.sprites_left = None
        self.sprites_right = None
        self.sprites_up = None
        self.sprites_down = None
        self.sprites = None
        self.sprites_index = 0  # needed to iterate through the list of sprites
        self.animation_length = 0.12  # controls speed of sprite animation

        # collisions:
        self.body = self.game.world.CreateDynamicBody(
            position=(
                self.x * self.game.physics_scale,
                self.y * self.game.physics_scale), userData=self)
        self.radius = 32
        fixture_def = b2FixtureDef(shape=b2CircleShape(
            radius=self.radius * self.game.physics_scale),
            friction=0.2, density=1.0)
        # fixture_def.filter.groupIndex = -2
        # noinspection PyUnusedLocal
        fixture = self.body.CreateFixture(fixture_def)

        # movement:
        self.current_tile_pos_char = None
        self.current_tile_pos_enemy = None
        self.path = None

    def destroy(self):
        self.game.world.DestroyBody(self.body)

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
        char = self.game.get_entity_of_category(CharacterEntity)
        tile_width = self.game.map.tilewidth
        tile_height = self.game.map.tileheight
        p1 = (self.x, self.y)
        new_tile_pos_enemy = (int(p1[0] / tile_width), int(p1[1] / tile_height))
        new_tile_pos_char = (char.x / tile_width, char.y)

        if char is not None:
            if self.current_tile_pos_enemy != new_tile_pos_enemy \
                    or self.current_tile_pos_char != new_tile_pos_char:
                self.current_tile_pos_enemy = new_tile_pos_enemy
                self.current_tile_pos_char = new_tile_pos_char

                # find path to char:
                self.path = PathFinder(self.game.map).find_path(p1, (char.x,
                                                                     char.y))

            if self.path is not None:
                # move towards next node:
                p2 = (self.path[1][0] * tile_width + tile_width / 2,
                      self.path[1][1] * tile_height + tile_height / 2)

                vector = (p2[0] - p1[0], p2[1] - p1[1])
                length = sqrt(vector[0] * vector[0] + vector[1] * vector[1])
                v_norm = (vector[0] / length, vector[1] / length)

                self.velocity = [v_norm[0] * speed, v_norm[1] * speed]

                # facing towards player:
                if abs(vector[1]) > abs(vector[0]):
                    if vector[1] < 0:
                        self.sprites = self.sprites_up
                    else:
                        self.sprites = self.sprites_down
                else:
                    if vector[0] < 0:
                        self.sprites = self.sprites_left
                    else:
                        self.sprites = self.sprites_right

    def render(self, surface, render_scale):
        sprite = self.sprites[self.sprites_index]
        sprite_w, sprite_h = sprite.get_size()[0], sprite.get_size()[1]
        tile_w, tile_h = self.game.map.tilewidth, self.game.map.tileheight
        sprite = pygame.transform.smoothscale(sprite,
                                              (int(sprite_w * render_scale[0]),
                                               int(sprite_h * render_scale[1])))
        surface.blit(sprite,
                     (int(((self.x - sprite_w / 2) * render_scale[0])),
                      int((self.y - sprite_h / 2) * render_scale[1])))

        super().render(surface, render_scale)

        if self.game.debugging and self.path is not None:
            # draw the enemy path:
            for index in range(len(self.path) - 1):
                pygame.draw.line(surface, (0, 0, 255),
                                 (self.path[index][0] * tile_w + tile_w / 2,
                                  self.path[index][1] * tile_h + tile_h / 2),
                                 (self.path[index + 1][0] * tile_w + tile_w / 2,
                                  self.path[index + 1][1] * tile_h + tile_h / 2))

            # calculate middle ray starting point and direction:
            char = self.game.get_entity_of_category(CharacterEntity)
            start2, finish = (self.x, self.y), (char.x, char.y)
            vector = (finish[0] - start2[0], finish[1] - start2[1])
            v_length = sqrt(vector[0] * vector[0] + vector[1] * vector[1])
            v_norm = (vector[0] / v_length, vector[1] / v_length)

            # calculate the starting point of the two outer rays:
            normal = (-v_norm[1], v_norm[0])
            start1 = (start2[0] + normal[0] * self.radius,
                      start2[1] + normal[1] * self.radius)
            start3 = (start2[0] - normal[0] * self.radius,
                      start2[1] - normal[1] * self.radius)

            # perform ray cast 1 and draw:
            callback = RayCastCallback()
            self.game.world.RayCast(callback,
                                    (start1[0] * self.game.physics_scale,
                                     start1[1] * self.game.physics_scale),
                                    (finish[0] * self.game.physics_scale,
                                     finish[1] * self.game.physics_scale))
            print('fraction 1 is ' + str(callback.fraction))
            pygame.draw.line(surface, (0, 0, 255), start1,
                             (start1[0] + v_norm[0] * v_length * callback.fraction,
                              start1[1] + v_norm[1] * v_length * callback.fraction))

            # perform ray cast 2 and draw:
            callback = RayCastCallback()
            self.game.world.RayCast(callback,
                                    (start2[0] * self.game.physics_scale,
                                     start2[1] * self.game.physics_scale),
                                    (finish[0] * self.game.physics_scale,
                                     finish[1] * self.game.physics_scale))
            print('fraction 2 is ' + str(callback.fraction))
            pygame.draw.line(surface, (0, 0, 255), start2,
                             (start2[0] + v_norm[0] * v_length * callback.fraction,
                              start2[1] + v_norm[1] * v_length * callback.fraction))

            # perform ray cast 3 and draw:
            callback = RayCastCallback()
            self.game.world.RayCast(callback,
                                    (start3[0] * self.game.physics_scale,
                                     start3[1] * self.game.physics_scale),
                                    (finish[0] * self.game.physics_scale,
                                     finish[1] * self.game.physics_scale))
            print('fraction 3 is ' + str(callback.fraction))
            pygame.draw.line(surface, (0, 0, 255), start3,
                             (start3[0] + v_norm[0] * v_length * callback.fraction,
                              start3[1] + v_norm[1] * v_length * callback.fraction))

    def synchronize_body(self):  # entity gives new info to body
        self.body.position = (self.x * self.game.physics_scale,
                              self.y * self.game.physics_scale)
        self.body.linearVelocity = (self.velocity[0] * self.game.physics_scale,
                                    self.velocity[1] * self.game.physics_scale)

    def synchronize_entity(self):  # body gives new info to entity
        self.x = self.body.position[0] / self.game.physics_scale
        self.y = self.body.position[1] / self.game.physics_scale
        self.velocity = [self.body.linearVelocity[0] / self.game.physics_scale,
                         self.body.linearVelocity[1] / self.game.physics_scale]
