from maze.game.entities.entity import Entity
from maze.game.entities.character_entity import CharacterEntity
import pygame


class EnemyEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.sprites_left = [pygame.image.load("data/images/enemy1/e1l1.png"),
                             pygame.image.load("data/images/enemy1/e1l2.png"),
                             pygame.image.load("data/images/enemy1/e1l3.png"),
                             pygame.image.load("data/images/enemy1/e1l4.png")]
        self.sprites_right = [pygame.image.load("data/images/enemy1/e1r1.png"),
                              pygame.image.load("data/images/enemy1/e1r2.png"),
                              pygame.image.load("data/images/enemy1/e1r3.png"),
                              pygame.image.load("data/images/enemy1/e1r4.png")]
        self.sprites_up = [pygame.image.load("data/images/enemy1/e1u1.png"),
                           pygame.image.load("data/images/enemy1/e1u2.png"),
                           pygame.image.load("data/images/enemy1/e1u3.png"),
                           pygame.image.load("data/images/enemy1/e1u4.png")]
        self.sprites_down = [pygame.image.load("data/images/enemy1/e1d1.png"),
                             pygame.image.load("data/images/enemy1/e1d2.png"),
                             pygame.image.load("data/images/enemy1/e1d3.png"),
                             pygame.image.load("data/images/enemy1/e1d4.png")]
        self.collision_rect = pygame.Rect(-100, 20, 200, 80)
        self.animation_length = 0.12  # controls speed of sprite animation
        self.sprite_index = 0  # needed to iterate through the list of sprites
        self.sprites = self.sprites_down
        self.solid = True
        self.x = 50
        self.y = 50

    def update(self, delta_time):
        # animating, used in render():
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.sprite_index += 1
            if self.sprite_index == 4:
                self.sprite_index = 0
            self.animation_length = 0.12

        speed = 50
        character = self.game.get_entity_of_category(CharacterEntity)
        if character is not None:
            # moving towards player:
            x_distance = self.x - character.x
            y_distance = self.y - character.y
            if abs(y_distance) < 1:
                self.y = character.y
            elif y_distance > 0:
                self.y -= speed * delta_time
            elif y_distance < 0:
                self.y += speed * delta_time
            if abs(x_distance) < 1:
                self.x = character.x
            elif x_distance < 0:
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
        sprite = self.sprites[self.sprite_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        surface.blit(sprite, (int(self.x - width/2), int(self.y - height/2)))
        super().render(surface)
