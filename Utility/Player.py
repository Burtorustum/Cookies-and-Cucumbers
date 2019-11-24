class Player:
    def __init__(self):
        self.held_item = None
        self.clues = []
        self.skills = []
        self.cur_room = None

    def is_holding_obj(self):
        return self.held_item is not None

    def has_skill(self, skill):
        return skill in self.skills

    def has_clue(self, clue):
        return clue in self.clues