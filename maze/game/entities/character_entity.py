from maze.game.entities.entity import Entity
from maze.game.entities.bullet_entity import BulletEntity
import pygame


class CharacterEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.char_u = pygame.image.load("data/images/char_up.png")
        self.char_d = pygame.image.load("data/images/char_down.png")
        self.char_l = pygame.image.load("data/images/char_left.png")
        self.char_r = pygame.image.load("data/images/char_right.png")

        self.move_u = True
        self.move_d = False
        self.move_l = False
        self.move_r = False

        self.shoot_u = False
        self.shoot_d = False
        self.shoot_l = False
        self.shoot_r = False

        self.x = 280
        self.y = 300

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        speed = 400

        # moving:
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move_u = True
            self.move_d, self.move_l, self.move_r = False, False, False
            self.y -= speed * delta_time
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.move_d = True
            self.move_u, self.move_l, self.move_r = False, False, False
            self.y += speed * delta_time
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.move_l = True
            self.move_u, self.move_d, self.move_r = False, False, False
            self.x -= speed * delta_time
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.move_r = True
            self.move_u, self.move_d, self.move_l = False, False, False
            self.x += speed * delta_time

        # shooting:
        if keys[pygame.K_UP]:
            self.shoot_u = True
            self.move_u, self.move_d, self.move_l, self.move_r= False, False, False, False
            self.shoot_d, self.shoot_l, self.shoot_r = False, False, False
            self.game.add_entity(BulletEntity(self.game, self.x, self.y))
        if keys[pygame.K_DOWN]:
            self.shoot_d = True
            self.move_u, self.move_d, self.move_l, self.move_r = False, False, False, False
            self.shoot_u, self.shoot_l, self.shoot_r = False, False, False
            self.game.add_entity(BulletEntity(self.game, self.x, self.y))
        if keys[pygame.K_LEFT]:
            self.shoot_l = True
            self.move_u, self.move_d, self.move_l, self.move_r = False, False, False, False
            self.shoot_u, self.shoot_d, self.shoot_r = False, False, False
            self.game.add_entity(BulletEntity(self.game, self.x, self.y))
        if keys[pygame.K_RIGHT]:
            self.shoot_r = True
            self.move_u, self.move_d, self.move_l, self.move_r = False, False, False, False
            self.shoot_u, self.shoot_d, self.shoot_l = False, False, False
            self.game.add_entity(BulletEntity(self.game, self.x, self.y))

    def render(self, surface):
        if self.shoot_u or self.move_u:
            surface.blit(self.char_u, (int(self.x), int(self.y)))
        if self.shoot_d or self.move_d:
            surface.blit(self.char_d, (int(self.x), int(self.y)))
        if self.shoot_l or self.move_l:
            surface.blit(self.char_l, (int(self.x), int(self.y)))
        if self.shoot_r or self.move_r:
            surface.blit(self.char_r, (int(self.x), int(self.y)))
