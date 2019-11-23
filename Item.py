class Item:
    def __init__(self, name, holdable, ):
        self.name = name
        self.holdable = holdable
        self.get_descriptions(name)

    def get_descriptions(self, name):
        pass
