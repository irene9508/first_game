import pygame

from maze.game.entities.entity import Entity


# class Particles(Entity):
#     def __init__(self, x, y, game, velocity, radius):
#         super().__init__(game)
#         self.velocity = velocity
#         self.x, self.y = x, y
#         self.radius = radius
#         self.timer = 5
#
#     def render(self, surface, render_scale):
#         pygame.draw.circle(surface, (255, 0, 0),
#                            (int(self.x * render_scale[0]),
#                             int(self.y * render_scale[1])),
#                            int(self.radius * render_scale[0]))
#
#         # movement
#         self.x += self.velocity[0]
#         self.y += self.velocity[1]
#
#         # decrease size over time:
#         if self.radius >= 0.5:
#             self.radius -= 0.01
#
#         # life duration:
#         self.timer -= 0.02
#         if self.timer <= 0:
#             self.timer = 5
#             self.marked_for_destroy = True


class ParticleEffectEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.particles = []
        self.timer = 5

    def add_particle(self, x, y, velocity, radius, surface, render_scale):
        self.particles.append(Particle(x, y, velocity, self.timer, radius))

        for particle in self.particles:
            particle.xy[0] += particle.velocity[0]
            particle.xy[1] += particle.velocity[1]
            particle.timer -= 0.02
            if particle.radius >= 0.02:
                particle.radius -= 0.01
            pygame.draw.circle(surface, (255, 0, 0),
                               (particle.xy[0] * render_scale[0],
                                particle.xy[1] * render_scale[1]),
                               particle.radius * render_scale[0])
            if particle.timer <= 0:
                self.particles.remove(particle)


class Particle:
    def __init__(self, x, y, velocity, timer, radius):
        self.xy = [x, y]
        self.velocity = velocity
        self.timer = timer
        self.radius = radius
