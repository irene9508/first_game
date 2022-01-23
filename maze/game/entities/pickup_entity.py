from maze.game.entities.entity import Entity


class PickupEntity(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.test = "pickup created"

    def create_pickup(self):
        print(self.test)
