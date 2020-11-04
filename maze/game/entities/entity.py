
class Entity:
    def __init__(self, game):
        self.marked_for_destroy = False
        self.rotation = 0.0
        self.game = game
        self.x = 0
        self.y = 0

    def destroy(self):
        pass

    def update(self, delta_time):
        pass

    def render(self, surface):
        pass
