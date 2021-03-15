import random
from math import cos, pi, sin

import pygame

from maze.game.entities.entity import Entity


class ParticleEffectEntity:
    def __init__(self, x, y, color, life_length):
        self.particles = []
        self.life_length = life_length
        self.new_particle_timer = 0
        self.color = color
        self.x = x
        self.y = y

    def render(self, surface, render_scale):
        for particle in self.particles:
            pygame.draw.circle(surface, self.color,
                               (int(particle.x * render_scale[0]),
                                int(particle.y * render_scale[1])),
                               int(particle.radius))

    def update(self, delta_time, speed, radius):

        angle = random.random() * 360
        velocity = [speed * cos(angle * pi / 180),
                    speed * sin(angle * pi / 180)]

        self.new_particle_timer -= delta_time
        if self.new_particle_timer <= 0:
            self.new_particle_timer = 0.005
            self.particles.append(
                Particle(self.x, self.y, velocity, self.life_length,
                         radius))
        for particle in self.particles:
            particle.x += particle.velocity[0]
            particle.y += particle.velocity[1]
            particle.life_length -= delta_time
            if particle.radius >= delta_time:
                particle.radius -= delta_time
            if particle.life_length <= 0:
                particle.marked_for_destroy = True

            # remove dead entities:
            new_entities = []
            for entity in self.particles:
                if entity.marked_for_destroy:
                    entity.destroy(self.particles)
                else:
                    new_entities.append(entity)
            self.particles = new_entities


class Particle:
    def __init__(self, x, y, velocity, life_length, radius):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.life_length = life_length
        self.radius = radius
        self.marked_for_destroy = False

    def destroy(self, particles):
        particles.remove(self)
