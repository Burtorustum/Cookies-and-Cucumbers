class Room:
    def __init__(self, name: str, objects: list, description: str):
        self.name = name
        self.objects = objects
        self.description = description

    # Returns the appropriate "Look Around" command response
    def look_around(self):
        return self.description + " As you look around, you see the following objects: " \
               + ", ".join([x.name for x in self.objects])
