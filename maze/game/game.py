import pygame

class Game:
    def __init__(self):
        self.entities = []
        self.entity_queue = []

    def update(self, delta_time):
        for entity1 in self.entities:
            entity1.update(delta_time)
        for entity1 in self.entities:
            if entity1.solid:
                for entity2 in self.entities:
                    if entity2 != entity1:
                        if entity2.solid:
                            self.solve_collision(entity1, entity2)
        self.initialize_entities()

    @staticmethod
    def solve_collision(entity1, entity2):
        rect1 = pygame.Rect(entity1.x + entity1.collision_rect.x,
                            entity1.y + entity1.collision_rect.y,
                            entity1.collision_rect.width,
                            entity1.collision_rect.height)
        rect2 = pygame.Rect(entity2.x + entity2.collision_rect.x,
                            entity2.y + entity2.collision_rect.y,
                            entity2.collision_rect.width,
                            entity2.collision_rect.height)

        diff1 = rect1.left - rect2.right
        diff2 = rect2.left - rect1.right
        diff3 = rect1.top - rect2.bottom
        diff4 = rect2.top - rect1.bottom

        if diff1 < 0 and diff2 < 0 and diff3 < 0 and diff4 < 0:
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
            if entity.marked_for_destroy:
                entity.destroy()
            else:
                new_entities.append(entity)
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
        for entity in self.entities:
            entity.debugging = not entity.debugging
