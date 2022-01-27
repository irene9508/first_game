from math import atan2, pi

import pygame

from pygame import image as img
from pygame.transform import flip

from maze.game.collision_masks import Category
from maze.game.enemy_state import EnemyState
from maze.game.entities.bullet_entity import BulletEntity
from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.enemy_entity import EnemyEntity


class EnemyEntityBlob(EnemyEntity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 10
        self.radius = 32
        self.create_new_body()

        # animation:
        self.img_r1 = [img.load("data/images/e1/e1side.png").convert_alpha()]
        self.img_l1 = [flip(img.load("data/images/e1/e1side.png").convert_alpha(), True, False)]
        self.img_up = [img.load("data/images/e1/e1u1.png").convert_alpha()]
        self.img_down = [img.load("data/images/e1/e1d1.png").convert_alpha()]
        self.img_dead = [img.load("data/images/e1/e1dead.png").convert_alpha()]
        self.img_dead_near = [img.load("data/images/e1/e1dead_near.png").convert_alpha()]
        self.images = self.img_down

    def attack(self, full_duration, current_duration):
        self.velocity = [0, 0]
        progress = current_duration / full_duration
        self.x = self.start_x + (self.goal_x - self.start_x) * progress
        self.y = self.start_y + (self.goal_y - self.start_y) * progress
        self.velocity = [0, 0]

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

    def retreat(self, full_duration, current_duration):
        super().retreat(full_duration, current_duration)
        self.velocity = [0, 0]
        progress = current_duration / full_duration
        self.x = self.goal_x + (self.start_x - self.goal_x) * progress
        self.y = self.goal_y + (self.start_y - self.goal_y) * progress
        self.velocity = [0, 0]

    def update(self, delta_time):
        super().update(delta_time)

        tile_width = self.game.map.tilewidth
        tile_height = self.game.map.tileheight
        char = self.game.get_entity_of_category(CharacterEntity)

        # shooting:
        shot_timer = 0.4
        self.initial_shot_timer -= delta_time
        walkable = self.check_if_walkable((int(char.x / tile_width), int(char.y / tile_height)))
        if walkable and self.state != EnemyState.dead:
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
