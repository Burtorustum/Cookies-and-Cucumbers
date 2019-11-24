from .Player import Player

class Interaction:

    """
    An Interaction represents the possible interaction texts that can appear when interacting with an object, where:
        - levels is the possible levels of interaction
        - text is a dictionary of levels and required skills, objects, or clues (keys) and the corresponding text (values)
        - required is the list of lists of possible skill, object, and clue combinations to interact with an object
        - level is the current level of interaction the player is on with the
        - fulfilled represents if the required objects have been collected and used, and will default to the
          "fulfilled" key in text; if there are no requirements, will default to None
    """
    def __init__(self, levels : int, text : dict, required=[], fulfilled=None, interactFunc=None):
        self.levels = levels
        self.text = text
        self.required = required
        self.currentLevel = 0
        self.fulfilled = fulfilled
        self.interactFunc = interactFunc

    # Changes the current interaction level by the given amount, bounding it within range [0, interaction.levels]
    def changeInteraction(self, changeAmount : int):
        self.currentLevel = max(0, min(self.level + changeAmount, self.levels))

    # Returns the appropriate response to "Interact" command,
    # with required objects taking precedence over interaction level
    # i.e. if a player is on interaction level 1 and also has gathered all required skills, objects, and clues to
    # interact with object, will return the latter interact text
    def getText(self, player : Player):
        if self.interactFunc is None:
            playerTools = player.skills.append(player.clues.append(player.held_obj))
            for items in self.required:
                fulfilled = all((lambda x : x in playerTools) for item in items)
                if fulfilled:
                    keyName = "".join(items)
                    self.fulfilled = True
                    return self.text[keyName]
            else:
                if self.fulfilled:
                    return self.text["fulfilled"]
                else:
                    self.changeInteraction(1)
                    return self.text[self.currentLevel]
        else:
            return self.interactFunc(self, player)
