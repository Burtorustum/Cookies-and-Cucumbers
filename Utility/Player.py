class Player:
    def __init__(self):
        self.held_obj = None
        self.clues = []
        self.skills = []
        self.cur_room = None

    def is_holding_obj(self, obj):
        return self.held_obj == obj

    def has_skill(self, skill):
        return skill in self.skills

    def has_clue(self, clue):
        return clue in self.clues