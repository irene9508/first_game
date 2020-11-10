class Screen:
    def __init__(self, app):
        self.app = app

    def process_event(self, event):
        pass

    def update(self, delta_time, screen_width, screen_height):
        pass

    def render(self, surface):
        pass
