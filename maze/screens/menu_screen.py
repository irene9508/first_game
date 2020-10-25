from maze.screens.screen import Screen
import pygame


class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.background = pygame.image.load("data/images/background2.jpg")
        self.letter = (255, 255, 255)
        self.shadow = (0, 0, 0)

        self.title_font = 'data/fonts/font1.ttf'
        self.title_size = pygame.font.Font(self.title_font, 120)
        self.title_shadow = self.title_size.render('MAZE', True, self.shadow)
        self.title = self.title_size.render('MAZE', True, self.letter)

        self.menu_font = 'data/fonts/font1.ttf'
        self.text = 'Press Enter to Start'
        self.menu_size = pygame.font.Font(self.menu_font, 32)
        self.menu_shadow = self.menu_size.render(self.text, True, self.shadow)
        self.menu = self.menu_size.render(self.text, True, self.letter)

    def process_event(self, event):
        pass

    def update(self):
        print("menu screen update")

    def render(self, surface):
        surface.blit(self.background, [0, 0])

        surface.blit(self.title_shadow, (27, 450))  # l/r, u/d
        surface.blit(self.title, (25, 450))

        surface.blit(self.menu_shadow, (502, 530))
        surface.blit(self.menu, (500, 530))
