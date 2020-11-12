import pygame
from maze.screens.screen_menu import ScreenMenu


class App:
    def __init__(self):
        self.running = True
        self.surface = None
        self.current_screen = None
        self.next_screen = None
        self.delta_time = 0
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 0

    def run(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.screen_width,
                                                self.screen_height))
        self.current_screen = ScreenMenu(self)
        fps_start_time = 0
        delta_start_time = 0
        fps_counter = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_screen.process_event(event)

            self.current_screen.update(self.delta_time)

            # calculate delta time:
            current_time = pygame.time.get_ticks()
            self.delta_time = (current_time - delta_start_time) / 1000
            delta_start_time = current_time

            # calculate fps:
            fps_counter += 1
            if current_time - fps_start_time > 1000:
                self.fps = fps_counter
                fps_counter = 0
                fps_start_time = current_time

            self.surface.fill((0, 0, 0))
            self.current_screen.render(self.surface)
            pygame.display.flip()

            self.process_screen_change()

        pygame.quit()

    def set_screen(self, screen):
        self.next_screen = screen

    def process_screen_change(self):
        if self.next_screen is not None:
            self.current_screen = self.next_screen
            self.next_screen = None
