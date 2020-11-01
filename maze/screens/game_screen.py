from maze.game.entities.character_entity import CharacterEntity
from maze.screens.screen import Screen
from maze.screens import menu_screen
from maze.game.game import Game
import pygame


class GameScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.game = Game()
        self.character = CharacterEntity(self.game)
        self.game.add_entity(self.character)
        self.delta_time = None

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.set_screen(menu_screen.MenuScreen(self.app))

    def update(self, delta_time):
        self.delta_time = delta_time
        self.game.update(delta_time)

    def render(self, surface):
        self.game.render(surface)
