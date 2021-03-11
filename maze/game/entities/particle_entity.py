import pygame

from maze.game.entities.entity import Entity


class Particles(Entity):
    def __init__(self, x, y, game, velocity, radius):
        super().__init__(game)
        self.velocity = velocity
        self.x, self.y = x, y
        self.radius = radius
        self.timer = 5

    def render(self, surface, render_scale):
        pygame.draw.circle(surface, (255, 0, 0),
                           (int(self.x * render_scale[0]),
                            int(self.y * render_scale[1])),
                           int(self.radius * render_scale[0]))

        # movement
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # decrease size over time:
        if self.radius >= 0.5:
            self.radius -= 0.01

        # life duration:
        self.timer -= 0.02
        if self.timer <= 0:
            self.timer = 5
            self.marked_for_destroy = True
