import pygame


class Game:
    def __init__(self):
        self.entities = []
        self.entity_queue = []
        self.debugging = False

    def update(self, delta_time, screen_width, screen_height):
        for entity1 in self.entities:
            entity1.update(delta_time, screen_width, screen_height)

        # check for collisions:
        for entity1 in self.entities:
            for entity2 in self.entities:
                if entity1 != entity2 and entity1.solid and entity2.solid:
                    self.find_collisions(entity1, entity2,
                                         entity1.collision_rect_solid,
                                         entity2.collision_rect_solid)
                if entity1 != entity2 and entity1.trigger and entity2.trigger:
                    self.find_collisions(entity1, entity2,
                                         entity1.collision_rect_trigger,
                                         entity2.collision_rect_trigger)

        self.initialize_entities()

    def find_collisions(self, entity1, entity2, coll_rect1, coll_rect2):
        rect1 = pygame.Rect(entity1.x + coll_rect1.x, entity1.y + coll_rect1.y,
                            coll_rect1.width, coll_rect1.height)
        rect2 = pygame.Rect(entity2.x + coll_rect2.x, entity2.y + coll_rect2.y,
                            coll_rect2.width, coll_rect2.height)

        diff1 = rect1.left - rect2.right
        diff2 = rect2.left - rect1.right
        diff3 = rect1.top - rect2.bottom
        diff4 = rect2.top - rect1.bottom

        if diff1 < 0 and diff2 < 0 and diff3 < 0 and diff4 < 0:
            # bump into each other:
            if entity1.solid and entity2.solid:
                self.solve_solid_collision(entity1, entity2, diff1, diff2,
                                           diff3, diff4)
            # trigger a reaction:
            if entity1.collision_group != 0 and entity2.collision_group != 0:
                if entity1.collision_group != entity2.collision_group:
                    if entity1.trigger and entity2.trigger:
                        entity1.solve_trigger_collision(entity2)
                        entity2.solve_trigger_collision(entity1)

    @staticmethod
    def solve_solid_collision(entity1, entity2, diff1, diff2, diff3, diff4):
        minimum = min(abs(diff1), abs(diff2), abs(diff3), abs(diff4))
        if minimum == abs(diff1):
            entity1.x -= diff1 * 0.5
            entity2.x += diff1 * 0.5
        elif minimum == abs(diff2):
            entity1.x += diff2 * 0.5
            entity2.x -= diff2 * 0.5
        elif minimum == abs(diff3):
            entity1.y -= diff3 * 0.5
            entity2.y += diff3 * 0.5
        elif minimum == abs(diff4):
            entity1.y += diff4 * 0.5
            entity2.y -= diff4 * 0.5

    def render(self, surface):
        self.entities.sort(key=lambda e: e.y)
        for entity in self.entities:
            entity.render(surface)

    def add_entity(self, entity):
        self.entity_queue.append(entity)

    def initialize_entities(self):
        # remove dead entities:
        new_entities = []
        for entity in self.entities:
            entity.destroy() if entity.marked_for_destroy \
                else new_entities.append(entity)
        self.entities = new_entities

        # add queued entities:
        self.entities.extend(self.entity_queue)
        self.entity_queue.clear()

    def get_entity_of_category(self, category):
        for entity in self.entities:
            if isinstance(entity, category):
                return entity
        return None

    def show_debug_info(self):
        self.debugging = not self.debugging
