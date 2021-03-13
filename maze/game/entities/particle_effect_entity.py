import pygame

from maze.game.entities.entity import Entity


class ParticleEffectEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.particles = []
        self.timer = 50
        self.x = None
        self.y = None

    def add_particle(self, x, y, velocity, radius):
        self.particles.append(Particle(x, y, velocity, self.timer, radius))

    def render(self, surface, render_scale):
        for particle in self.particles:
            particle.x += particle.velocity[0]
            particle.y += particle.velocity[1]
            particle.timer -= 0.02
            if particle.radius >= 0.02:
                particle.radius -= 0.01
            pygame.draw.circle(surface, (255, 0, 0),
                               (int(particle.x * render_scale[0]),
                                int(particle.y * render_scale[1])),
                               int(particle.radius * render_scale[0]))
            if particle.timer <= 0:
                self.particles.remove(particle)


class Particle:
    def __init__(self, x, y, velocity, timer, radius):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.timer = timer
        self.radius = radius
