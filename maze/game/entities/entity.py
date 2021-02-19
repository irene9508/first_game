from maze.game.room_change_behavior import RoomChangeBehavior


class Entity:
    def __init__(self, game):

        # properties:
        self.game = game
        self.marked_for_destroy = False
        self.rotation = 0.0
        self.x = 0
        self.y = 0
        self.active = True
        self.room = game.room
        self.room_change_behavior = RoomChangeBehavior.nothing

    def activate(self):
        self.active = True

    def contact(self, fixture, other_fixture, contact):
        pass

    def deactivate(self):
        self.active = False

    def destroy(self):
        pass

    def render(self, surface, render_scale):
        pass

    def synchronize_body(self):
        pass

    def synchronize_entity(self):
        pass

    def trigger_collision_reaction(self, entity):
        pass

    def update(self, delta_time):
        pass
