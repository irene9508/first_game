import pygame

from maze.screens import game_screen
from maze.screens.screen import Screen


class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.background = pygame.image.load("data/images/bg2.jpg")
        self.letter_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)
        self.font = 'data/fonts/font2.ttf'

        self.title_size = pygame.font.Font(self.font, 120)
        self.title_shadow = self.title_size.render('MAZE', True, self.shadow_color)
        self.title = self.title_size.render('MAZE', True, self.letter_color)

        self.menu_size = pygame.font.Font(self.font, 32)
        self.text = 'Press Enter to Start'
        self.menu_shadow = self.menu_size.render(self.text, True, self.shadow_color)
        self.menu = self.menu_size.render(self.text, True, self.letter_color)

        self.tutorial_size = pygame.font.Font(self.font, 32)
        self.text = 'WASD to move. Arrow keys to shoot. E to interact. R to restart. M to mute.'
        self.tutorial_shadow = self.tutorial_size.render(self.text, True, self.shadow_color)
        self.tutorial = self.tutorial_size.render(self.text, True, self.letter_color)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.running = False
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.app.set_screen(game_screen.GameScreen(self.app))

    def render(self, surface, r_scale):
        width = self.background.get_size()[0]
        height = self.background.get_size()[1]
        background = pygame.transform.smoothscale(self.background, (int(width * r_scale[0]),
                                                                    int(height * r_scale[1])))
        surface.blit(background, (0, 0))

        surface_width = surface.get_size()[0]
        surface_height = surface.get_size()[1]
        surface.blit(self.title_shadow, (20, surface_height - 150))
        surface.blit(self.title, (15, surface_height - 155))

        surface.blit(self.menu_shadow, (202, surface_height - 65))
        surface.blit(self.menu, (200, surface_height - 67))

        surface.blit(self.tutorial_shadow, (surface_width - 668, surface_height - 65))
        surface.blit(self.tutorial, (surface_width - 670, surface_height - 67))

    def update(self, delta_time):
        pass
