from math import sqrt

import pygame
from Box2D import b2FixtureDef, b2CircleShape, b2RayCastCallback, b2_staticBody
from pygame import mixer

from maze.game.collision_masks import Category
from maze.game.enemy_state import EnemyState
from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.entity import Entity
from maze.game.particle_effect import ParticleEffect
from maze.game.path_finder import PathFinder
from maze.game.room_change_behavior import RoomChangeBehavior


class RayCastCallback(b2RayCastCallback):
    def __init__(self):
        b2RayCastCallback.__init__(self)
        self.fraction = 1

    def ReportFixture(self, fixture, point, normal, fraction):
        if fixture.body.type != b2_staticBody:
            return -1
        self.fraction = fraction
        # report how far the ray goes before bumping into something:
        return fraction


class EnemyEntity(Entity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game)

        # properties:
        self.distance = None
        self.attack_duration = None
        self.room_change_behavior = RoomChangeBehavior.deactivate
        self.state = EnemyState.following
        self.velocity = [0, 0]
        self.x = spawn_x
        self.y = spawn_y
        self.health = 0

        # animation:
        self.animation_length = 0.12  # controls speed of sprite animation
        self.img_dead_near = None
        self.img_r1 = None
        self.img_dead = None
        self.img_down = None
        self.img_l1 = None
        self.r_scale = None
        self.surface = None
        self.img_index = 0  # needed to iterate through the list of images
        self.img_up = None
        self.images = None

        # collisions:
        self.radius = None
        self.body = None

        # movement:
        self.current_tile_pos_enemy = None
        self.current_retreat_duration = 0
        self.current_tile_pos_char = None
        self.current_attack_duration = 0
        self.start_x = None
        self.start_y = None
        self.goal_x = None
        self.goal_y = None
        self.path = None

        # shooting:
        self.shot_sound = mixer.Sound('data/sounds/laser.wav')
        self.initial_shot_timer = 0.5

        # particles:
        self.particles = []

    def activate(self):
        super().activate()
        self.state = EnemyState.following
        self.create_new_body()

    def attack(self, full_duration, current_duration):
        pass

    def check_if_walkable(self, end_point):
        # calculate middle ray starting point and direction:
        start2 = (self.x, self.y)
        tile_width = self.game.map.tilewidth
        tile_height = self.game.map.tileheight
        finish2 = (end_point[0] * tile_width + tile_width / 2,
                   end_point[1] * tile_height + tile_height / 2)
        vector = (finish2[0] - start2[0], finish2[1] - start2[1])
        v_length = sqrt(vector[0] * vector[0] + vector[1] * vector[1])
        v_norm = (vector[0] / v_length, vector[1] / v_length)

        # calculate the starting point of the two outer rays:
        normal = (-v_norm[1], v_norm[0])
        start1 = (start2[0] + normal[0] * self.radius,
                  start2[1] + normal[1] * self.radius)
        start3 = (start2[0] - normal[0] * self.radius,
                  start2[1] - normal[1] * self.radius)
        finish1 = (finish2[0] + normal[0] * self.radius,
                   finish2[1] + normal[1] * self.radius)
        finish3 = (finish2[0] - normal[0] * self.radius,
                   finish2[1] - normal[1] * self.radius)

        # perform ray casts:
        callback1 = RayCastCallback()
        self.game.world.RayCast(callback1,
                                (start1[0] * self.game.physics_scale,
                                 start1[1] * self.game.physics_scale),
                                (finish1[0] * self.game.physics_scale,
                                 finish1[1] * self.game.physics_scale))
        callback2 = RayCastCallback()
        self.game.world.RayCast(callback2,
                                (start2[0] * self.game.physics_scale,
                                 start2[1] * self.game.physics_scale),
                                (finish2[0] * self.game.physics_scale,
                                 finish2[1] * self.game.physics_scale))
        callback3 = RayCastCallback()
        self.game.world.RayCast(callback3,
                                (start3[0] * self.game.physics_scale,
                                 start3[1] * self.game.physics_scale),
                                (finish3[0] * self.game.physics_scale,
                                 finish3[1] * self.game.physics_scale))

        # if there are no obstructions:
        if callback1.fraction == callback2.fraction == callback3.fraction == 1:
            return True
        else:
            return False

    def contact(self, fixture, other_fixture, contact):
        if isinstance(other_fixture.body.userData, CharacterEntity):
            if self.state != EnemyState.dead:
                other_fixture.body.userData.health -= 5
                self.particles.append(
                    ParticleEffect(other_fixture.body.userData.x, other_fixture.body.userData.y,
                                   (0, 0, 0), [1, 5], [2, 7], [2, 20], 60, 0))

    def create_new_body(self):
        self.body = self.game.world.CreateDynamicBody(
            position=(self.x * self.game.physics_scale,
                      self.y * self.game.physics_scale),
            userData=self)
        fixture_def = b2FixtureDef(
            shape=b2CircleShape(radius=self.radius * self.game.physics_scale),
            friction=0.2, density=1.0, categoryBits=Category.ENEMY,
            maskBits=(Category.ENEMY | Category.CHARACTER |
                      Category.CHARACTER_BULLET | Category.WALL |
                      Category.CORPSE))
        # noinspection PyUnusedLocal
        fixture = self.body.CreateFixture(fixture_def)

    def destroy(self):
        self.game.world.DestroyBody(self.body)

    def die(self):
        self.velocity = [0, 0]
        if self.distance < 80:
            self.images = self.img_dead_near
        else:
            self.images = self.img_dead

    def render(self, surface, r_scale):
        self.r_scale, self.surface = r_scale, surface
        super().render(surface, r_scale)

        # particles:
        for item in self.particles:
            item.render(surface, r_scale)

        # enemy path:
        if self.game.debugging and self.path is not None:
            tile_w = self.game.map.tilewidth
            tile_h = self.game.map.tileheight
            end_pos = (self.path[0][0] * r_scale[0] * tile_w + tile_w / 2,
                       self.path[0][1] * r_scale[1] * tile_w + tile_w / 2)
            pygame.draw.line(surface, (0, 0, 255), (self.x, self.y), end_pos)
            for index in range(len(self.path) - 1):
                pygame.draw.line(
                    surface, (0, 0, 255),
                    (self.path[index][0] * r_scale[0] * tile_w + tile_w / 2,
                     self.path[index][1] * r_scale[1] * tile_h + tile_h / 2),
                    (self.path[index + 1][0] * tile_w * r_scale[0] + tile_w / 2,
                     self.path[index + 1][1] * tile_h * r_scale[
                         1] + tile_h / 2))

    def retreat(self, full_duration, current_duration):
        pass

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

    def take_damage(self, damage):
        self.body.userData.health -= damage
        self.particles.append(ParticleEffect(self.x, self.y, (0, 0, 0), [1, 5], [2, 7], [2, 20],
                                             60, 0))

    def update(self, delta_time):
        # animation, used in render():
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.img_index += 1
            if self.img_index == len(self.images):
                self.img_index = 0
            self.animation_length = 0.12

        # health:
        if self.health <= 0:
            self.state = EnemyState.dead
            self.body.fixtures[0].filterData.categoryBits = Category.CORPSE
            self.body.fixtures[0].filterData.maskBits = (
                    Category.CHARACTER_BULLET | Category.ENEMY_BULLET |
                    Category.CHARACTER | Category.ENEMY | Category.WALL |
                    Category.CORPSE)

        # movement:
        speed = 150
        tile_width = self.game.map.tilewidth
        tile_height = self.game.map.tileheight
        p1 = (self.x, self.y)
        char = self.game.get_entity_of_category(CharacterEntity)
        new_tile_pos_enemy = (int(p1[0] / tile_width), int(p1[1] / tile_height))
        self.distance = sqrt((char.x - self.x) ** 2 + (char.y - self.y) ** 2)
        new_tile_pos_char = (char.x / tile_width, char.y / tile_height)
        game_map = self.game.map
        self.attack_duration = 0.2

        if char is not None:
            if self.state == EnemyState.following:
                if self.current_tile_pos_enemy != new_tile_pos_enemy \
                        or self.current_tile_pos_char != new_tile_pos_char:
                    # find path to char:
                    self.current_tile_pos_enemy = new_tile_pos_enemy
                    self.current_tile_pos_char = new_tile_pos_char
                    self.path = PathFinder(game_map).find_path(
                        p1, (char.x, char.y))

                if self.path is not None:
                    # skip nodes that aren't needed:
                    while len(self.path) >= 2:
                        walkable = self.check_if_walkable(self.path[1])
                        if walkable:
                            del (self.path[0])
                        else:
                            break

                    # move towards next node:
                    p2 = (self.path[0][0] * tile_width + tile_width / 2,
                          self.path[0][1] * tile_height + tile_height / 2)
                    vector = (p2[0] - p1[0], p2[1] - p1[1])
                    length = sqrt(vector[0] * vector[0] + vector[1] * vector[1])
                    v_norm = (vector[0] / length, vector[1] / length)
                    if self.active:
                        self.velocity = [v_norm[0] * speed, v_norm[1] * speed]

                    # face towards player:
                    if abs(vector[1]) > abs(vector[0]):
                        if vector[1] < 0:
                            self.images = self.img_up
                        else:
                            self.images = self.img_down
                    else:
                        if vector[0] < 0:
                            self.images = self.img_l1
                        else:
                            self.images = self.img_r1

                # detect whether to attack:
                if self.distance < 80:
                    self.state = EnemyState.attacking
                    self.start_x, self.start_y = self.x, self.y
                    self.goal_x, self.goal_y = char.x, char.y
                    self.current_attack_duration = 0

            elif self.state == EnemyState.attacking:
                self.current_attack_duration += delta_time
                if self.current_attack_duration < self.attack_duration:
                    self.attack(self.attack_duration, self.current_attack_duration)
                else:
                    self.particles.append(ParticleEffect(char.x, char.y, (0, 0, 0), [1, 5], [2, 7],
                                                         [2, 20], 60, 0))
                    self.state = EnemyState.retreating
                    self.current_retreat_duration = 0
                    char.health -= 5

            elif self.state == EnemyState.retreating:
                self.current_retreat_duration += delta_time
                if self.current_retreat_duration < self.attack_duration:
                    self.retreat(self.attack_duration, self.current_retreat_duration)
                else:
                    self.state = EnemyState.following

            elif self.state == EnemyState.dead:
                self.die()

        # particles:
        for item in self.particles:
            item.x = self.x
            item.y = self.y
            item.update(delta_time)
