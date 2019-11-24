from .Utility import Item


class Room:

    def __init__(self, name: str, objects: set, description: str, adjRooms: list):
        self.name = name
        self.objects = objects
        self.description = description
        self.adjRooms = adjRooms

    # Returns the appropriate "Look Around" command response
    def lookAround(self):
        return self.description + " As you look around, you see the following objects: " \
               + ", ".join([x.name for x in self.objects])