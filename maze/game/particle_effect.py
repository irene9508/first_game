import random
from math import cos, pi, sin

import pygame


class ParticleEffect:
    def __init__(self, x, y, color, life_span, speed, radius, first_burst, emission_rate):
        self.emission_rate = emission_rate
        self.new_particle_timer = 0
        self.life_span = life_span  # tuple of integers
        self.radius = radius  # tuple of integers
        self.particles = []
        self.speed = speed  # tuple of integers
        self.color = color  # rgb
        self.x = x
        self.y = y

        # initial burst:
        for x in range(first_burst):
            angle = random.random() * 360
            radian = angle * pi / 180
            speed = random.randint(self.speed[0], self.speed[1]) / 5
            velocity = [speed * cos(radian), speed * sin(radian)]
            life_span = random.randint(self.life_span[0], self.life_span[1]) / 10
            radius = random.randint(self.radius[0], self.radius[1])

            self.particles.append(Particle(self.x, self.y, velocity, life_span, radius))

    def render(self, surface, render_scale):
        for particle in self.particles:
            x = int(particle.x * render_scale[0])
            y = int(particle.y * render_scale[1])
            pygame.draw.circle(surface, self.color, (x, y), int(particle.radius))

    def update(self, delta_time):
        angle = random.random() * 360
        radian = angle * pi / 180
        speed = self.speed[0] / 10
        velocity = [speed * cos(radian), speed * sin(radian)]

        # add new particles:
        self.new_particle_timer -= delta_time
        if self.new_particle_timer <= 0 and self.emission_rate != 0:
            self.new_particle_timer = 0.005
            self.particles.append(
                Particle(self.x, self.y, velocity, self.life_span,
                         random.randint(self.radius[0], self.radius[1])))

        # change existing particles:
        for particle in self.particles:
            particle.velocity[0] *= 0.98
            particle.velocity[1] *= 0.98
            particle.x += particle.velocity[0]
            particle.y += particle.velocity[1]
            particle.life_span -= delta_time
            if particle.radius >= delta_time:
                particle.radius -= 20 * delta_time
                if particle.radius < 0:
                    particle.radius = 0
            if particle.life_span <= 0:
                particle.marked_for_destroy = True

        # remove dead particles:
        new_particles = []
        for particle in self.particles:
            if particle.marked_for_destroy:
                particle.destroy(self.particles)
            else:
                new_particles.append(particle)
        self.particles = new_particles


class Particle:
    def __init__(self, x, y, velocity, life_span, radius):
        self.marked_for_destroy = False
        self.life_span = life_span
        self.velocity = velocity
        self.radius = radius
        self.x = x
        self.y = y

    def destroy(self, particles):
        particles.remove(self)
