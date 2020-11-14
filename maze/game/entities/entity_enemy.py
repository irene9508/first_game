from maze.game.entities.entity import Entity
from maze.game.entities.entity_character import EntityCharacter
import pygame


class EntityEnemy(Entity):
    def __init__(self, game):
        super().__init__(game)

        # properties:
        self.health = 0
        self.x = 100
        self.y = 100

        # animation:
        self.sprites_left = [pygame.image.load("data/images/bullet.png").convert_alpha()]
        self.sprites_right = [pygame.image.load("data/images/bullet.png").convert_alpha()]
        self.sprites_up = [pygame.image.load("data/images/bullet.png").convert_alpha()]
        self.sprites_down = [pygame.image.load("data/images/bullet.png").convert_alpha()]
        self.sprites = self.sprites_down
        self.sprites_index = 0  # needed to iterate through the list of sprites
        self.animation_length = 0.12  # controls speed of sprite animation

        # collisions:
        self.collision_group = 2
        self.solid = True
        self.solid_collision_box = pygame.Rect(0, 0, 0, 0)
        self.trigger = True
        self.trigger_collision_box = pygame.Rect(0, 0, 0, 0)

    def update(self, delta_time):
        # animation, used in render():
        self.animation_length -= delta_time
        if self.animation_length <= 0:
            self.sprites_index += 1
            if self.sprites_index == len(self.sprites):
                self.sprites_index = 0
            self.animation_length = 0.12

        # health:
        if self.health <= 0:
            self.marked_for_destroy = True

        # movement:
        speed = 50
        character = self.game.get_entity_of_category(EntityCharacter)
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
