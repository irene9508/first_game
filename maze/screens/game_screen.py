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

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.set_screen(menu_screen.MenuScreen(self.app))
            if event.key == pygame.K_COMMA:
                self.game.show_debug_info()
            if event.key == pygame.K_r:
                self.app.set_screen(GameScreen(self.app))

    def update(self, delta_time):
        self.game.update(delta_time)
        if self.game.debugging:
            print(self.app.fps)

    def render(self, surface):
        self.game.render(surface)
