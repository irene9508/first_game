from maze.game.entities.character_entity import CharacterEntity
from maze.game.entities.enemy_entity_blob import EnemyEntityBlob
from maze.screens.screen import Screen
from maze.screens import menu_screen
from maze.game.game import Game
import pygame


class GameScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.game = Game()
        self.game.load()
        self.character = CharacterEntity(self.game)
        self.enemy = EnemyEntityBlob(self.game)
        self.game.add_entity(self.character)
        self.game.add_entity(self.enemy)
        self.path = None

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.set_screen(menu_screen.MenuScreen(self.app))
            if event.key == pygame.K_COMMA:
                self.game.show_debug_info()
            if event.key == pygame.K_r:
                self.app.set_screen(GameScreen(self.app))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game.debugging:
                self.path = self.game.find_path((self.character.x + self.character.solid_collision_box.centerx,
                                                 self.character.y + self.character.solid_collision_box.centery),
                                                pygame.mouse.get_pos())
                print(self.path)  # [(9, 2), (10, 3), (11, 3), (12, 4)]

    def update(self, delta_time):
        self.game.update(delta_time)
        if self.game.debugging:
            print(self.app.fps)

    def render(self, surface):
        self.game.render(surface)
        if self.game.debugging:
            if self.path is not None:
                for index in range(len(self.path) - 1):
                    pygame.draw.line(surface, (0, 0, 255),
                                     (self.path[index][0] * self.game.map.tilewidth + self.game.map.tilewidth / 2,
                                      self.path[index][1] * self.game.map.tileheight + self.game.map.tileheight / 2),
                                     (self.path[index + 1][0] * self.game.map.tilewidth + self.game.map.tilewidth / 2,
                                      self.path[index + 1][1] * self.game.map.tileheight + self.game.map.tileheight / 2))
