import pygame.draw
import pygame.pixelarray
from Box2D import b2Draw


class MyDraw(b2Draw):
    def __init__(self, app):
        super().__init__()
        self.app = app

    # (color[0] * 255, color[1] * 255, color[2] * 255)
    # (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
    # (int(center[0]), int(center[1]))

    # noinspection PyPep8Naming
    def DrawCircle(self, center, radius, color, drawwidth=1):
        pygame.draw.circle(self.app.surface,
                           (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)),
                           (int(center[0]), int(center[1])),
                           int(radius))

    # noinspection PyPep8Naming
    def DrawSolidCircle(self, center, radius, axis, color):
        self.DrawCircle((int(center[0]), int(center[1])), int(radius),
                        (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))

    # noinspection PyPep8Naming
    def DrawPoint(self, point, size, color):
        pygame.Surface.set_at(point,
                              (color[0] * 255, color[1] * 255, color[2] * 255))

    # noinspection PyPep8Naming
    def DrawPolygon(self, vertices, vertex_count, color):
        pygame.draw.polygon(self.app.surface,
                            (color[0] * 255, color[1] * 255, color[2] * 255),
                            vertices)

    # noinspection PyPep8Naming
    def DrawSolidPolygon(self, vertices, vertex_count, color):
        self.DrawPolygon(vertices, vertex_count,
                         (color[0] * 255, color[1] * 255, color[2] * 255))
