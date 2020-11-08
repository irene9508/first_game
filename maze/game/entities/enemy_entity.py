from maze.game.entities.entity import Entity
from maze.game.entities.character_entity import CharacterEntity
import pygame


class EnemyEntity(Entity):
    def __init__(self, game):
        super().__init__(game)

        self.sprites_left = [pygame.image.load("data/images/enemy2/e2l1.png"),
                             pygame.image.load("data/images/enemy2/e2l2.png"),
                             pygame.image.load("data/images/enemy2/e2l3.png"),
                             pygame.image.load("data/images/enemy2/e2l4.png")]
        self.sprites_right = [pygame.image.load("data/images/enemy2/e2r1.png"),
                              pygame.image.load("data/images/enemy2/e2r2.png"),
                              pygame.image.load("data/images/enemy2/e2r3.png"),
                              pygame.image.load("data/images/enemy2/e2r4.png")]
        self.sprites_up = [pygame.image.load("data/images/enemy3/e3r1.png"),
                           pygame.image.load("data/images/enemy3/e3r1.png"),
                           pygame.image.load("data/images/enemy3/e3r1.png"),
                           pygame.image.load("data/images/enemy3/e3r1.png")]
        self.sprites_down = [pygame.image.load("data/images/enemy1/e1d1.png"),
                             pygame.image.load("data/images/enemy1/e1d2.png"),
                             pygame.image.load("data/images/enemy1/e1d3.png"),
                             pygame.image.load("data/images/enemy1/e1d4.png")]

        self.sprites = self.sprites_down
        self.sprites_index = 0  # needed to iterate through the list of sprites

        self.animation_length = 0.12  # controls speed of sprite animation
        self.collision_rect_solid = pygame.Rect(-100, 20, 200, 80)
        self.collision_rect_trigger = pygame.Rect(-100, 20, 200, 80)
        self.height = self.sprites[0].get_size()
        self.solid = True
        self.trigger = True
        self.width = self.sprites[0].get_size()
        self.x = 50
        self.y = 50

    def update(self, delta_time):
        # animating, used in render():
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.sprites_index += 1
            if self.sprites_index == 4:
                self.sprites_index = 0
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
        sprite = self.sprites[self.sprites_index]
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        surface.blit(sprite, (int(self.x - width/2), int(self.y - height/2)))
        super().render(surface)
