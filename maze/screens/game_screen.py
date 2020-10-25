from maze.game.entities.character_entity import CharacterEntity
from maze.screens.screen import Screen
from maze.screens import menu_screen
from maze.game.game import Game
import pygame


class GameScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.game = Game()
        self.game.add_entity(CharacterEntity(self.game))

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.set_screen(menu_screen.MenuScreen(self.app))

    def update(self):
        self.game.update()

    def render(self, surface):
        self.game.render(surface)
