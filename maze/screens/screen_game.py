from maze.game.entities.entity_character import EntityCharacter
from maze.game.entities.entity_enemy_blob import EntityEnemyBlob
from maze.screens.screen import Screen
from maze.screens import screen_menu
from maze.game.game import Game
import pygame


class ScreenGame(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.game = Game()
        self.game.load()
        self.character = EntityCharacter(self.game)
        self.enemy = EntityEnemyBlob(self.game)
        self.game.add_entity(self.character)
        self.game.add_entity(self.enemy)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.set_screen(screen_menu.ScreenMenu(self.app))
            if event.key == pygame.K_COMMA:
                self.game.show_debug_info()

    def update(self, delta_time):
        self.game.update(delta_time)
        if self.game.debugging:
            print(self.app.fps)

    def render(self, surface):
        self.game.render(surface)
