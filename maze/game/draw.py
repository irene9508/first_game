import pygame.draw
import pygame.pixelarray
from Box2D import b2Draw


class Draw(b2Draw):
	def __init__(self, app):
		super().__init__()
		self.app = app

	def draw_circle(self, color, center_xy, radius, drawwidth=1):
		""" Draw a wireframe circle given the center,
		radius, axis of orientation and color.  """
		pygame.draw.circle(self.app.surface, color, center_xy, radius)

	def draw_point(self, color, point_xy, size=1):
		""" Draw a single point at point p given a pixel size and color.  """
		pygame.PixelArray(self.app.surface)[point_xy[0]][point_xy[1]] = color

	def draw_polygon(self, color, corner_xy):
		""" Draw a wireframe polygon given the screen vertices
		(tuples) with the specified color.  """
		pygame.draw.polygon(self.app.surface, color, corner_xy)

	# - https: // github.com / pybox2d / pybox2d / wiki / manual  # debug-drawing
	# use somewhere but idk where
	# draw = MyDraw()
	# world = b2World()
	# world.renderer = draw
