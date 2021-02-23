import pygame.draw
from pygame import gfxdraw
import pygame.pixelarray

from Box2D import b2Draw


# noinspection PyMethodOverriding,PyPep8Naming
class MyDraw(b2Draw):
    def __init__(self, app, physics_scale):
        super().__init__()
        self.app = app
        self.physics_scale = physics_scale

    def DrawCircle(self, center, radius, color, drawwidth=1):
        pygame.draw.circle(
            self.app.surface,
            (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)),
            (int(center[0] / self.physics_scale * self.app.render_scale[0]),
             int(center[1] / self.physics_scale * self.app.render_scale[1])),
            int(radius / self.physics_scale * self.app.render_scale[0]))

    def DrawSolidCircle(self, center, radius, axis, color):
        self.DrawCircle(center, radius, color)

    # noinspection PyUnusedLocal
    def DrawPoint(self, p, size, color):
        gfxdraw.pixel(self.app.surface,
                      p[0] / self.physics_scale * self.app.render_scale[0],
                      p[1] / self.physics_scale * self.app.render_scale[1],
                      (color[0] * 255, color[1] * 255, color[2] * 255))
        # self.app.surface.set_at(
        #     (p[0] / self.physics_scale * self.app.render_scale[0],
        #      p[1] / self.physics_scale * self.app.render_scale[1]),
        #     (color[0] * 255, color[1] * 255, color[2] * 255))

    def DrawPolygon(self, vertices, color):
        pygame.draw.polygon(
            self.app.surface, (color[0] * 255, color[1] * 255, color[2] * 255),
            ((vertices[0][0] / self.physics_scale * self.app.render_scale[0],
              vertices[0][1] / self.physics_scale * self.app.render_scale[1]),
             (vertices[1][0] / self.physics_scale * self.app.render_scale[0],
              vertices[1][1] / self.physics_scale * self.app.render_scale[1]),
             (vertices[2][0] / self.physics_scale * self.app.render_scale[0],
              vertices[2][1] / self.physics_scale * self.app.render_scale[1]),
             (vertices[3][0] / self.physics_scale * self.app.render_scale[0],
              vertices[3][1] / self.physics_scale * self.app.render_scale[1])))

    def DrawSolidPolygon(self, vertices, color):
        self.DrawPolygon(vertices, color)
