import random
from math import cos, pi, sin

import pygame


class ParticleEffect:
    def __init__(self, x, y, color, life_length, speed, radius, initial_burst, emission_rate):
        self.initial_burst = initial_burst
        self.emission_rate = emission_rate
        self.life_length = life_length
        self.new_particle_timer = 0
        self.radius = radius
        self.particles = []
        self.color = color
        self.speed = speed
        self.x = x
        self.y = y

        # initial burst:
        for x in range(initial_burst):
            angle = random.random() * 360
            velocity = [self.speed * cos(angle * pi / 180),
                        self.speed * sin(angle * pi / 180)]
            self.particles.append(
                Particle(self.x, self.y, velocity, self.life_length,
                         random.randint(self.radius[0], self.radius[1])))

    def render(self, surface, render_scale):
        for particle in self.particles:
            pygame.draw.circle(
                surface, self.color, (int(particle.x * render_scale[0]),
                                      int(particle.y * render_scale[1])),
                int(particle.radius))

    def update(self, delta_time):
        angle = random.random() * 360
        velocity = [self.speed * cos(angle * pi / 180),
                    self.speed * sin(angle * pi / 180)]

        self.new_particle_timer -= delta_time
        if self.new_particle_timer <= 0 and self.emission_rate != 0:
            self.new_particle_timer = 0.005
            self.particles.append(
                Particle(self.x, self.y, velocity, self.life_length,
                         random.randint(self.radius[0], self.radius[1])))
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
