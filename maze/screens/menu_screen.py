import pygame

from maze.screens.screen import Screen

class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)

    def update(self):
        print("menu screen update")
