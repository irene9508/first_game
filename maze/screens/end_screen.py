import pygame

from maze.game.game import Game
from maze.screens import menu_screen
from maze.screens.screen import Screen


class EndScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.title = None
        self.title_shadow = None
        self.background = pygame.image.load("data/images/bg2.jpg")
        self.game = Game
        self.app = app

        self.letter_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)
        self.font = 'data/fonts/font2.ttf'

        self.title_size = pygame.font.Font(self.font, 120)
        self.title_shadow = self.title_size.render('YOU WON!', True, self.shadow_color)
        self.title = self.title_size.render('YOU WON!', True, self.letter_color)

        self.menu_size = pygame.font.Font(self.font, 32)
        self.text = 'Enter to return to main menu. Escape to exit.'
        self.menu_shadow = self.menu_size.render(self.text, True, self.shadow_color)
        self.menu = self.menu_size.render(self.text, True, self.letter_color)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.app.set_screen(menu_screen.MenuScreen(self.app))
            if event.key == pygame.K_ESCAPE:
                self.app.running = False

    def render(self, surface, r_scale):
        width = self.background.get_size()[0]
        height = self.background.get_size()[1]
        background = pygame.transform.smoothscale(self.background, (int(width * r_scale[0]),
                                                                    int(height * r_scale[1])))
        surface.blit(background, (0, 0))

        surface_height = surface.get_size()[1]
        surface.blit(self.title_shadow, (20, surface_height - 150))
        surface.blit(self.title, (15, surface_height - 155))

        surface.blit(self.menu_shadow, (327, surface_height - 60))
        surface.blit(self.menu, (325, surface_height - 62))

    def update(self, delta_time):
        pass
