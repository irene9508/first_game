from maze.screens.screen import Screen
import pygame


class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.background_image = None

    def run(self):
        self.background_image = pygame.image.load("background1")

    def process_event(self, event):
        pass

    def update(self):
        print("menu screen update")
