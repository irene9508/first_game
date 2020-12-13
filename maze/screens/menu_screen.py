import pygame

from maze.screens import game_screen
from maze.screens.screen import Screen


class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.background = pygame.image.load("data/images/bg.jpg")
        self.letter = (255, 255, 255)
        self.shadow = (0, 0, 0)

        self.title_font = 'data/fonts/font2.ttf'
        self.title_size = pygame.font.Font(self.title_font, 120)
        self.title_shadow = self.title_size.render('MAZE', True, self.shadow)
        self.title = self.title_size.render('MAZE', True, self.letter)

        self.menu_font = 'data/fonts/font2.ttf'
        self.menu_size = pygame.font.Font(self.menu_font, 32)
        self.text = 'Press Enter to Start'
        self.menu_shadow = self.menu_size.render(self.text, True, self.shadow)
        self.menu = self.menu_size.render(self.text, True, self.letter)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.running = False
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.app.set_screen(game_screen.GameScreen(self.app))

    def update(self, delta_time):
        pass

    def render(self, surface, render_scale):
        width, height = self.background.get_size()[0], self.background.get_size()[1]
        background = pygame.transform.smoothscale(
            self.background,
            (int(width * render_scale[0]), int(height * render_scale[1])))
        surface.blit(background, (0, 0))

        surface_width = surface.get_size()[0]
        surface_height = surface.get_size()[1]
        surface.blit(self.title_shadow, (20, surface_height - 150))  # (horizontal, vertical)
        surface.blit(self.title, (15, surface_height - 155))

        surface.blit(self.menu_shadow, (202, surface_height - 65))
        surface.blit(self.menu, (200, surface_height - 67))
