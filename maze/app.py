import os
import random

import pygame
import sys
if sys.platform == "win32":
    import ctypes

from maze.screens.menu_screen import MenuScreen
from os import environ


class App:
    def __init__(self):
        self.current_screen = None
        self.delta_time = 0
        self.fps = 0
        self.playing = False
        self.next_screen = None
        self.ref_res = (1280, 720)  # reference resolution
        self.running = True
        self.render_scale = None
        self.surface = None

    def process_screen_change(self):
        if self.next_screen is not None:
            self.current_screen = self.next_screen
            self.next_screen = None

    def run(self):
        if sys.platform == "win32":
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        monitor_size = [pygame.display.Info().current_w,
                        pygame.display.Info().current_h]
        self.surface = pygame.display.set_mode(
            (1280, 720), flags=pygame.RESIZABLE)
        self.current_screen = MenuScreen(self)
        fullscreen = False

        fps_start_time = 0
        delta_start_time = 0
        fps_counter = 0

        # game loop:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:
                    if not fullscreen:
                        self.surface = pygame.display.set_mode(
                            (event.w, event.h), flags=pygame.RESIZABLE)

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        self.surface = pygame.display.set_mode(
                            monitor_size, flags=pygame.FULLSCREEN)
                    else:
                        self.surface = pygame.display.set_mode(
                            (1280, 720), flags=pygame.RESIZABLE)

                else:
                    self.current_screen.process_event(event)

            # play background music:
            if not self.playing:
                path = "data/sounds/music/"
                all_music = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]
                randomfile = random.choice(all_music)
                print(randomfile)
                pygame.mixer.init()
                pygame.mixer.music.load(randomfile)
                pygame.mixer.music.play()
                self.playing = True

            # update screens:
            self.current_screen.update(self.delta_time)
            current_time = pygame.time.get_ticks()

            # calculate delta time:
            self.delta_time = (current_time - delta_start_time) / 1000
            delta_start_time = current_time

            # calculate fps:
            fps_counter += 1
            if current_time - fps_start_time > 1000:
                self.fps = fps_counter
                fps_counter = 0
                fps_start_time = current_time

            self.render_scale = (self.surface.get_size()[0] / self.ref_res[0],
                                 self.surface.get_size()[1] / self.ref_res[1])

            self.current_screen.render(self.surface, self.render_scale)
            pygame.display.flip()

            self.process_screen_change()

        pygame.quit()

    def set_screen(self, screen):
        self.next_screen = screen
