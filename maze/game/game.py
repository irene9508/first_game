class Game:
    def __init__(self):
        self.entities = []
        self.entity_queue = []

    def update(self, delta_time):
        for entity in self.entities:
            entity.update(delta_time)
        self.initialize_entities()

    def render(self, surface):
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
