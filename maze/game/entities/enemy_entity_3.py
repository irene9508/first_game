import pygame
from pygame import image as img
from pygame.transform import flip

from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.enemy_entity import EnemyEntity


class EnemyEntityArnt(EnemyEntity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 8
        self.radius = 38
        self.create_new_body()

        # animation:
        self.img_l1 = [img.load("data/images/e3/e3-1.png").convert_alpha()]
        self.img_l2 = [img.load("data/images/e3/e3-2.png").convert_alpha()]
        self.img_l3 = [img.load("data/images/e3/e3-3.png").convert_alpha()]
        self.img_l4 = [img.load("data/images/e3/e3-4.png").convert_alpha()]
        self.img_l5 = [img.load("data/images/e3/e3-5.png").convert_alpha()]

        self.img_r1 = [flip(img.load("data/images/e3/e3-1.png").convert_alpha(), True, False)]
        self.img_r2 = [flip(img.load("data/images/e3/e3-2.png").convert_alpha(), True, False)]
        self.img_r3 = [flip(img.load("data/images/e3/e3-3.png").convert_alpha(), True, False)]
        self.img_r4 = [flip(img.load("data/images/e3/e3-4.png").convert_alpha(), True, False)]
        self.img_r5 = [flip(img.load("data/images/e3/e3-5.png").convert_alpha(), True, False)]

        self.imgs_left = [self.img_l1, self.img_l2, self.img_l3, self.img_l4, self.img_l5]
        self.imgs_right = [self.img_r1, self.img_r2, self.img_r3, self.img_r4, self.img_r5]

        self.img_up = [img.load("data/images/e3/e3-1.png").convert_alpha()]
        self.img_down = [img.load("data/images/e3/e3-1.png").convert_alpha()]
        self.img_dead = [img.load("data/images/e3/e3dead.png").convert_alpha()]
        self.img_dead_near = [img.load("data/images/e3/e3dead.png").convert_alpha()]
        self.images = self.img_down

    def attack(self, full_duration, current_duration):
        self.velocity = [0, 0]
        progress = current_duration / full_duration
        char = self.game.get_entity_of_category(CharacterEntity)
        if self.x >= char.x:
            image = int(progress * len(self.imgs_left))
            self.images = self.imgs_left[image]
        elif self.x < char.x:
            image = int(progress * len(self.imgs_right))
            self.images = self.imgs_right[image]
        self.velocity = [0, 0]

    def render(self, surface, r_scale):
        self.r_scale, self.surface = r_scale, surface
        sprite = self.images[self.img_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        r_size = (int(width * r_scale[0]), int(height * r_scale[1]))
        sprite = pygame.transform.smoothscale(sprite, r_size)
        r_position = (int(((self.x - width / 2) * r_scale[0])),
                      int((self.y - height / 2 - 80) * r_scale[1]))

        surface.blit(sprite, r_position)
        super().render(surface, r_scale)

    def retreat(self, full_duration, current_duration):
        self.velocity = [0, 0]
        progress = current_duration / full_duration
        if self.images in self.imgs_left:
            image = int((1 - progress) * len(self.imgs_left))
            self.images = self.imgs_left[image]
        elif self.images in self.imgs_right:
            image = int((1 - progress) * len(self.imgs_right))
            self.images = self.imgs_right[image]
        self.velocity = [0, 0]
