from maze.game.entities.entity import Entity
from maze.game.entities.character_entity import CharacterEntity
import pygame


class EnemyEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.sprites = [pygame.image.load("data/images/enemy1.png"),
                        pygame.image.load("data/images/enemy2.png"),
                        pygame.image.load("data/images/enemy3.png"),
                        pygame.image.load("data/images/enemy4.png")]
        self.animation_length = 0.12  # controls speed of sprite animation
        self.sprite_index = 0  # needed to iterate through the list of sprites
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

        # moving towards player:
        speed = 100
        character = self.game.get_entity_of_category(CharacterEntity)
        if character is not None:
            x_distance = self.x - character.x
            y_distance = self.y - character.y
            if x_distance > 0:
                self.x -= speed * delta_time
            if y_distance > 0:
                self.y -= speed * delta_time
            if x_distance < 0:
                self.x += speed * delta_time
            if y_distance < 0:
                self.y += speed * delta_time
            print(x_distance, y_distance)
            # if distance is positive, subtract a value (each loop)to get closer
            # to character. If distance is negative, add a value.

    def render(self, surface):
        sprite = pygame.transform.rotate(self.sprites[self.sprite_index],
                                         self.rotation)
        width, height = sprite.get_size()[0], sprite.get_size()[1]
        surface.blit(sprite, (int(self.x - width / 2),
                              int(self.y - height / 2)))
