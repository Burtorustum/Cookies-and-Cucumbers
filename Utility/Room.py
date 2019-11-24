class Room:
    def __init__(self, name, objects, description):
        self.name = name
        self.objects = objects
        self.description = description

    def update_desc(self, update):
        self.description = update
