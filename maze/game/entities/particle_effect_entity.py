import pygame

from maze.game.entities.entity import Entity


class ParticleEffectEntity(Entity):
    def __init__(self, game, x, y, velocity, radius):
        super().__init__(game)
        self.particles = []
        self.timer = 50
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
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
    def __init__(self, x, y, velocity, timer, radius):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.timer = timer
        self.radius = radius
        self.marked_for_destroy = False

    def destroy(self, particles):
        particles.remove(self)
