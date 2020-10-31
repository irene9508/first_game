
class Entity:
    def __init__(self, game):
        self.x = 400
        self.y = 400
        self.rotation = 0.0
        self.game = game
        self.marked_for_destroy = False

    def destroy(self):
        pass

    def update(self):
        pass

    def render(self, surface):
        pass
