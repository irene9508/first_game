from math import sqrt, atan2, pi

import pygame
from Box2D import b2FixtureDef, b2CircleShape, b2RayCastCallback, b2_staticBody
from pygame import mixer

from maze.game.collision_masks import Category
from maze.game.enemy_state import EnemyState
from maze.game.entities.bullet_entity import BulletEntity
from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.entity import Entity
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
        self.room_change_behavior = RoomChangeBehavior.deactivate
        self.state = EnemyState.following
        self.health = 0
        self.x = spawn_x
        self.y = spawn_y
        self.velocity = [0, 0]

        # animation:
        self.animation_length = 0.12  # controls speed of sprite animation
        self.img_right = None
        self.img_dead = None
        self.img_down = None
        self.img_left = None
        self.img_index = 0  # needed to iterate through the list of images
        self.img_up = None
        self.images = None
        self.r_scale = None
        self.surface = None

        # collisions:
        self.radius = 32
        self.body = None
        self.create_new_body()

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

    def activate(self):
        super().activate()
        self.state = EnemyState.following
        self.create_new_body()

    def attack(self, full_duration, current_duration):
        # where we're at in the animation:
        progress = current_duration / full_duration
        self.x = self.start_x + (self.goal_x - self.start_x) * progress
        self.y = self.start_y + (self.goal_y - self.start_y) * progress

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

        # perform ray cast 1:
        callback1 = RayCastCallback()
        self.game.world.RayCast(callback1,
                                (start1[0] * self.game.physics_scale,
                                 start1[1] * self.game.physics_scale),
                                (finish1[0] * self.game.physics_scale,
                                 finish1[1] * self.game.physics_scale))

        # perform ray cast 2:
        callback2 = RayCastCallback()
        self.game.world.RayCast(callback2,
                                (start2[0] * self.game.physics_scale,
                                 start2[1] * self.game.physics_scale),
                                (finish2[0] * self.game.physics_scale,
                                 finish2[1] * self.game.physics_scale))

        # perform ray cast 3:
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

    def create_new_body(self):
        self.body = self.game.world.CreateDynamicBody(
            position=(self.x * self.game.physics_scale,
                      self.y * self.game.physics_scale),
            userData=self)
        fixture_def = b2FixtureDef(
            shape=b2CircleShape(radius=self.radius * self.game.physics_scale),
            friction=0.2,
            density=1.0,
            categoryBits=Category.ENEMY,
            maskBits=(Category.ENEMY | Category.CHARACTER |
                      Category.CHARACTER_BULLET | Category.WALL |
                      Category.CORPSE))
        # noinspection PyUnusedLocal
        fixture = self.body.CreateFixture(fixture_def)

    def destroy(self):
        self.game.world.DestroyBody(self.body)

    def render(self, surface, r_scale):
        self.r_scale, self.surface = r_scale, surface
        sprite = self.images[self.img_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        r_size = (int(width * r_scale[0]), int(height * r_scale[1]))
        sprite = pygame.transform.smoothscale(sprite, r_size)
        r_position = (int(((self.x - width / 2) * r_scale[0])),
                      int((self.y - height / 2) * r_scale[1]))

        surface.blit(sprite, r_position)
        super().render(surface, r_scale)

        # draw the enemy path:
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
        progress = current_duration / full_duration
        self.x = self.goal_x + (self.start_x - self.goal_x) * progress
        self.y = self.goal_y + (self.start_y - self.goal_y) * progress

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
        distance = sqrt((char.x - self.x) ** 2 + (char.y - self.y) ** 2)
        new_tile_pos_char = (char.x / tile_width, char.y / tile_height)
        game_map = self.game.map
        duration = 0.07

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
                            self.images = self.img_left
                        else:
                            self.images = self.img_right

                # detect whether to attack:
                if distance < 80:
                    self.state = EnemyState.attacking
                    self.start_x, self.start_y = self.x, self.y
                    self.goal_x, self.goal_y = char.x, char.y
                    self.current_attack_duration = 0

            elif self.state == EnemyState.attacking:
                self.current_attack_duration += delta_time
                if self.current_attack_duration < duration:
                    self.velocity = [0, 0]
                    self.attack(duration, self.current_attack_duration)
                    self.velocity = [0, 0]
                else:
                    self.velocity = [0, 0]
                    self.state = EnemyState.retreating
                    self.current_retreat_duration = 0

            elif self.state == EnemyState.retreating:
                self.current_retreat_duration += delta_time
                if self.current_retreat_duration < duration:
                    self.velocity = [0, 0]
                    self.retreat(duration, self.current_retreat_duration)
                    self.velocity = [0, 0]
                else:
                    self.velocity = [0, 0]
                    self.state = EnemyState.following

            elif self.state == EnemyState.dead:
                self.images = self.img_dead
                self.velocity = [0, 0]
                if distance < 80:
                    pass

        # shooting:
        shot_timer = 0.5
        self.initial_shot_timer -= delta_time
        walkable = self.check_if_walkable(
            (int(char.x / tile_width), int(char.y / tile_height)))
        if walkable and self.state != EnemyState.dead:
            self.images = self.img_up
            delta_x = char.x - self.x
            delta_y = char.y - self.y
            angle = atan2(delta_y, delta_x) * 180 / pi
            if self.initial_shot_timer <= 0:
                pygame.mixer.stop()
                self.shot_sound.play()
                self.initial_shot_timer = shot_timer
                self.game.add_entity(BulletEntity(
                    self.game, self.x, self.y, angle, Category.ENEMY_BULLET,
                    Category.CHARACTER | Category.WALL | Category.CORPSE))
