import pygame


class Particles:
    def __init__(self, x, y, surface, r_scale):
        self.timer = 3
        self.particle(x, y, surface, r_scale)
        # self.velocity =

    def particle(self, x, y, surface, r_scale):
        pygame.draw.circle(surface, (255, 255, 255),
                           (int(x * r_scale[0]),
                            int(y * r_scale[1])),
                           int(2 * r_scale[0]))

        # shot_timer = 0.2
        # self.initial_shot_timer -= delta_time
        # if self.initial_shot_timer <= 0:
        #     self.initial_shot_timer = shot_timer
