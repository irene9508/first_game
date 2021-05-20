import pygame
from pygame import image as img

from maze.game.entities.enemy_entity import EnemyEntity


class EnemyEntityArnt(EnemyEntity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 8
        self.radius = 20
        self.create_new_body()

        # animation:
        self.img_l1 = [img.load("data/images/e3/e3l1.png").convert_alpha()]
        self.img_l2 = [img.load("data/images/e3/e3l2.png").convert_alpha()]
        self.img_l3 = [img.load("data/images/e3/e3l3.png").convert_alpha()]
        self.img_l4 = [img.load("data/images/e3/e3l4.png").convert_alpha()]
        self.img_l5 = [img.load("data/images/e3/e3l5.png").convert_alpha()]

        self.img_r1 = [img.load("data/images/e3/e3r1.png").convert_alpha()]
        self.img_r2 = [img.load("data/images/e3/e3r2.png").convert_alpha()]
        self.img_r3 = [img.load("data/images/e3/e3r3.png").convert_alpha()]
        self.img_r4 = [img.load("data/images/e3/e3r4.png").convert_alpha()]
        self.img_r5 = [img.load("data/images/e3/e3r5.png").convert_alpha()]

        self.imgs_right = [self.img_r1, self.img_r2, self.img_r3, self.img_r4, self.img_r5]
        self.imgs_left = [self.img_l1, self.img_l2, self.img_l3, self.img_l4, self.img_l5]

        self.img_up = [img.load("data/images/e3/e3r1.png").convert_alpha()]
        self.img_down = [img.load("data/images/e3/e3r1.png").convert_alpha()]
        self.img_dead = [img.load("data/images/e1/e1dead.png").convert_alpha()]
        self.img_dead_near = [img.load("data/images/e1/e1dead.png").convert_alpha()]
        self.images = self.img_down

    def attack(self, full_duration, current_duration):
        progress = current_duration / full_duration
        if self.images in self.imgs_left:
            image = int(progress * len(self.imgs_left))
            print(image, progress)
            self.images = self.imgs_left[image]
        elif self.images in self.imgs_right:
            image = int(progress * len(self.imgs_right))
            print(image, progress)
            self.images = self.imgs_right[image]

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
        progress = current_duration / full_duration
        if self.images in self.imgs_left:
            image = int((1 - progress) * len(self.imgs_left))
            print(image, progress)
            self.images = self.imgs_left[image]
        elif self.images in self.imgs_right:
            image = int((1 - progress) * len(self.imgs_right))
            print(image, progress)
            self.images = self.imgs_right[image]
