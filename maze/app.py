import pygame
from maze.screens.menu_screen import MenuScreen


class App:
    def __init__(self):
        self.running = True
        self.surface = None
        self.current_screen = MenuScreen(self)
        self.next_screen = None

    def run(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_screen.process_event(event)

            self.current_screen.update()

            self.surface.fill((0, 0, 0))
            self.current_screen.render()
            pygame.display.flip()

            self.process_screen_change()

        pygame.quit()

    def set_screen(self, screen):
        self.next_screen = screen

    def process_screen_change(self):
        if self.next_screen is not None:
            self.current_screen = self.next_screen
            self.next_screen = None
