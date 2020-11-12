from maze.screens.screen import Screen
from maze.screens import screen_game
import pygame


class ScreenMenu(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.background = pygame.image.load("data/images/background.jpg")
        self.letter = (255, 255, 255)
        self.shadow = (0, 0, 0)

        self.title_font = 'data/fonts/font2.ttf'
        self.title_size = pygame.font.Font(self.title_font, 120)
        self.title_shadow = self.title_size.render('MAZE', True, self.shadow)
        self.title = self.title_size.render('MAZE', True, self.letter)

        self.menu_font = 'data/fonts/font2.ttf'
        self.menu_size = pygame.font.Font(self.menu_font, 32)
        self.menu_text = 'Press Enter to Start'
        self.menu_shadow = self.menu_size.render(self.menu_text, True, self.shadow)
        self.menu = self.menu_size.render(self.menu_text, True, self.letter)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.running = False
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.app.set_screen(screen_game.ScreenGame(self.app))

    def update(self, delta_time):
        pass

    def render(self, surface):
        surface.blit(self.background, [0, 0])

        surface.blit(self.title_shadow, (27, 570))  # (horizontal, vertical)
        surface.blit(self.title, (25, 570))

        surface.blit(self.menu_shadow, (202, 660))
        surface.blit(self.menu, (200, 660))
