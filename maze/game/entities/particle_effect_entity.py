import random

import pygame

from maze.game.entities.entity import Entity


class ParticleEffectEntity(Entity):
    def __init__(self, game, x, y):
        super().__init__(game)
        self.particles = []
        self.end_life_timer = 5
        self.new_particle_timer = 1
        self.x = x
        self.y = y
        self.particles.append(Particle(
            self.x, self.y, [random.randint(-100, 100) / 500, random.randint(-100, 100) / 500],
            self.end_life_timer, random.randint(2, 15)))

    def render(self, surface, render_scale):
        for particle in self.particles:
            particle.x += particle.velocity[0]
            particle.y += particle.velocity[1]
            particle.end_life_timer -= 0.02
            if particle.radius >= 0.02:
                particle.radius -= 0.01
            pygame.draw.circle(surface, (255, 0, 0),
                               (int(particle.x * render_scale[0]),
                                int(particle.y * render_scale[1])),
                               int(particle.radius * render_scale[0]))
            if particle.end_life_timer <= 0:
                particle.marked_for_destroy = True

            # remove dead entities:
            new_entities = []
            for entity in self.particles:
                if entity.marked_for_destroy:
                    entity.destroy(self.particles)
                else:
                    new_entities.append(entity)
            self.particles = new_entities

    def update(self, delta_time):
        self.new_particle_timer -= delta_time
        if self.new_particle_timer <= 0:
            self.particles.append(
                Particle(
                    self.x, self.y,
                    [random.randint(-100, 100) / 500,
                     random.randint(-100, 100) / 500],
                    self.end_life_timer, random.randint(2, 15)))


class Particle:
    def __init__(self, x, y, velocity, timer, radius):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.end_life_timer = timer
        self.radius = radius
        self.marked_for_destroy = False

    def destroy(self, particles):
        particles.remove(self)
