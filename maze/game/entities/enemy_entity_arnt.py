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
        self.img_left1 = [img.load("data/images/e3/e3l1.png").convert_alpha()]
        self.img_left2 = [img.load("data/images/e3/e3l2.png").convert_alpha()]
        self.img_left3 = [img.load("data/images/e3/e3l3.png").convert_alpha()]
        self.img_left4 = [img.load("data/images/e3/e3l4.png").convert_alpha()]
        self.img_left5 = [img.load("data/images/e3/e3l5.png").convert_alpha()]

        self.img_right1 = [img.load("data/images/e3/e3r1.png").convert_alpha()]
        self.img_right2 = [img.load("data/images/e3/e3r2.png").convert_alpha()]
        self.img_right3 = [img.load("data/images/e3/e3r3.png").convert_alpha()]
        self.img_right4 = [img.load("data/images/e3/e3r4.png").convert_alpha()]
        self.img_right5 = [img.load("data/images/e3/e3r5.png").convert_alpha()]

        self.img_up = [img.load("data/images/e3/e3r1.png").convert_alpha()]
        self.img_down = [img.load("data/images/e3/e3r1.png").convert_alpha()]
        self.img_dead = [img.load("data/images/e1/e1dead.png").convert_alpha()]
        self.img_dead_near = [img.load("data/images/e1/e1dead.png").convert_alpha()]
        self.images = self.img_down

    def attack(self, full_duration, current_duration):
        progress = current_duration / full_duration
        if self.images == self.img_left1 or self.images == self.img_left2 or self.images == self.img_left3 or self.images == self.img_left4 or self.images == self.img_left5:
            if progress <= 0.2:
                self.images = self.img_left1
            elif progress <= 0.4:
                self.images = self.img_left2
            elif progress <= 0.6:
                self.images = self.img_left3
            elif progress <= 0.8:
                self.images = self.img_left4
            elif progress <= 1:
                self.images = self.img_left5
        elif self.images == self.img_right1 or self.images == self.img_right2 or self.images == self.img_right3 or self.images == self.img_right4 or self.images == self.img_right5:
            if progress <= 0.2:
                self.images = self.img_right1
            elif progress <= 0.4:
                self.images = self.img_right2
            elif progress <= 0.6:
                self.images = self.img_right3
            elif progress <= 0.8:
                self.images = self.img_right4
            elif progress <= 1:
                self.images = self.img_right5

    def render(self, surface, r_scale):
        self.r_scale, self.surface = r_scale, surface
        sprite = self.images[self.img_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        r_size = (int(width * r_scale[0]), int(height * r_scale[1]))
        sprite = pygame.transform.smoothscale(sprite, r_size)
        r_position = (int(((self.x - width / 2 - 20) * r_scale[0])),
                      int((self.y - height / 2 - 80) * r_scale[1]))

        surface.blit(sprite, r_position)
        super().render(surface, r_scale)

    def retreat(self, full_duration, current_duration):
        progress = current_duration / full_duration
        if self.images == self.img_left1 or self.images == self.img_left2 or self.images == self.img_left3 or self.images == self.img_left4 or self.images == self.img_left5:
            if progress <= 0.2:
                self.images = self.img_left5
            elif progress <= 0.4:
                self.images = self.img_left4
            elif progress <= 0.6:
                self.images = self.img_left3
            elif progress <= 0.8:
                self.images = self.img_left2
            elif progress <= 1:
                self.images = self.img_left1
        elif self.images == self.img_right1 or self.images == self.img_right2 or self.images == self.img_right3 or self.images == self.img_right4 or self.images == self.img_right5:
            if progress <= 0.2:
                self.images = self.img_right5
            elif progress <= 0.4:
                self.images = self.img_right4
            elif progress <= 0.6:
                self.images = self.img_right3
            elif progress <= 0.8:
                self.images = self.img_right2
            elif progress <= 1:
                self.images = self.img_right1
