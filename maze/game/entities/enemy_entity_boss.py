import pygame

from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.enemy_entity import EnemyEntity
from pygame.transform import flip
from pygame import image as img
from maze.game.entities.pickup_entity import PickupEntity


class EnemyEntityBoss(EnemyEntity):
    def __init__(self, game, spawn_x, spawn_y):
        super().__init__(game, spawn_x, spawn_y)

        # properties:
        self.health = 5
        self.radius = 25
        self.create_new_body()

        # animation:
        self.img_l1 = [pygame.image.load("data/images/e2/e2l1.png").convert_alpha()]
        self.img_r1 = [
            flip(img.load("data/images/e2/e2l1.png").convert_alpha(), True, False)
        ]
        self.img_up = [pygame.image.load("data/images/e2/e2l1.png").convert_alpha()]
        self.img_down = [pygame.image.load("data/images/e2/e2l1.png").convert_alpha()]
        self.img_dead = [pygame.image.load("data/images/e2/e2l1.png").convert_alpha()]
        self.img_dead_near = [img.load("data/images/e2/e2l1.png").convert_alpha()]
        self.images = self.img_down

    def die(self):
        char = self.game.get_entity_of_category(CharacterEntity)
        self.marked_for_destroy = True
        self.game.add_entity(PickupEntity(self.game, self.x, self.y))

    def render(self, surface, r_scale):
        self.r_scale, self.surface = r_scale, surface
        sprite = self.images[self.img_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        r_size = (int(width * r_scale[0]), int(height * r_scale[1]))
        sprite = pygame.transform.smoothscale(sprite, r_size)
        r_position = (
            int((self.x - width / 2) * r_scale[0]),
            int((self.y - height / 2) * r_scale[1]),
        )

        surface.blit(sprite, r_position)
        super().render(surface, r_scale)
