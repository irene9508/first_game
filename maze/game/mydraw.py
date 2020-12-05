import pygame.draw
import pygame.pixelarray
from Box2D import b2Draw


# noinspection PyMethodOverriding
class MyDraw(b2Draw):
    def __init__(self, app, physics_scale):
        super().__init__()
        self.app = app
        self.physics_scale = physics_scale

    # noinspection PyPep8Naming
    def DrawCircle(self, center, radius, color, drawwidth=1):
        pygame.draw.circle(self.app.surface,
                           (int(color[0] * 255), int(color[1] * 255),
                            int(color[2] * 255)),
                           (int(center[0] / self.physics_scale),
                            int(center[1] / self.physics_scale)),
                           int(radius * self.physics_scale))

    # noinspection PyPep8Naming
    def DrawSolidCircle(self, center, radius, axis, color):
        self.DrawCircle(center, radius, color)

    # noinspection PyPep8Naming
    def DrawPoint(self, point, size, color):
        pygame.Surface.set_at(
            (point[0] / self.physics_scale, point[1] / self.physics_scale),
            (color[0] * 255, color[1] * 255, color[2] * 255))

    # noinspection PyPep8Naming
    def DrawPolygon(self, vertices, color):
        pygame.draw.polygon(self.app.surface,
                            (color[0] * 255, color[1] * 255, color[2] * 255),
                            ((vertices[0][0] / self.physics_scale,
                             vertices[0][1] / self.physics_scale),
                             (vertices[1][0] / self.physics_scale,
                             vertices[1][1] / self.physics_scale),
                             (vertices[2][0] / self.physics_scale,
                              vertices[2][1] / self.physics_scale),
                             (vertices[3][0] / self.physics_scale,
                              vertices[3][1] / self.physics_scale)))

    # noinspection PyPep8Naming
    def DrawSolidPolygon(self, vertices, color):
        self.DrawPolygon(vertices, color)
