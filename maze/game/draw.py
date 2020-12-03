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

	def draw_point(self, point_xy, size, color):
		""" Draw a single point at point p given a pixel size and color.  """
		pygame.Surface.set_at(point_xy, color)

	def draw_polygon(self, corner_xy, color):
		""" Draw a wireframe polygon given the screen vertices
		(tuples) with the specified color.  """
		pygame.draw.polygon(self.app.surface, color, corner_xy)

	# - https: // github.com / pybox2d / pybox2d / wiki / manual  # debug-drawing
	# use somewhere but idk where
	# draw = MyDraw()
	# world = b2World()
	# world.renderer = draw
