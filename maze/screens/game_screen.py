import pygame

from maze.game.entities.character_entity import CharacterEntity
from maze.game.path_finder import PathFinder
from maze.game.game import Game
from maze.screens import menu_screen
from maze.screens.screen import Screen


class GameScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.game = Game(self.app)
        self.game.load('data/Tiled/room1.tmx')
        self.char = CharacterEntity(self.game)
        self.game.add_entity(self.char)
        self.path = None

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.set_screen(menu_screen.MenuScreen(self.app))
            if event.key == pygame.K_COMMA:
                self.game.show_debug_info()
            if event.key == pygame.K_r:
                self.app.set_screen(GameScreen(self.app))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # todo: does this work?
            if self.game.debugging:
                self.path = PathFinder(self.game.map).find_path(
                    (self.char.x, self.char.y), pygame.mouse.get_pos())

    def render(self, surface, r_scale):
        self.game.render(surface, r_scale)

        index = 0
        for hp in range(self.char.health):
            while index < self.char.health:
                pygame.draw.circle(
                    surface, (0, 0, 0), (5 * index + 20, 20), 7)
                pygame.draw.circle(
                    surface, (255, 0, 0), (5 * index + 20, 20), 5)
                index += 5

        tile_width = self.game.map.tilewidth
        tile_height = self.game.map.tileheight
        if self.game.debugging and self.path is not None:
            # draw the path from character to mouse click:
            for index in range(len(self.path) - 1):
                pygame.draw.line(
                    surface, (0, 0, 255),
                    (self.path[index][0] * tile_width + tile_width / 2,
                     self.path[index][1] * tile_height + tile_height / 2),
                    (self.path[index + 1][0] * tile_width + tile_width / 2,
                     self.path[index + 1][1] * tile_height + tile_height / 2))

    def update(self, delta_time):
        self.game.update(delta_time)
        if self.game.debugging:
            print(self.app.fps)
        if self.char.health <= 0:
            self.app.set_screen(menu_screen.MenuScreen(self.app))
