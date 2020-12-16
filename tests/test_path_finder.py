from unittest import TestCase
from maze.game.path_finder import PathFinder
from pytmx.util_pygame import load_pygame
import pygame


class TestPathFinder(TestCase):
    def test_find_path(self):
        # surface is included, otherwise an error occurs
        surface = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE)
        test_map = load_pygame('data/test_map.tmx')
        start = (40, 40)
        finish = (200, 40)
        actual_value = PathFinder(test_map).find_path(start, finish)
        expected_value = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0)]
        self.assertEqual(expected_value, actual_value)
