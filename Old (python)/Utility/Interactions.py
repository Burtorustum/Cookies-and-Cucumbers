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

    def __init__(self, levels: int, text: dict, required=[], fulfilled=None, interactFunc=None):
        self.levels = levels
        self.text = text
        self.required = required
        self.currentLevel = 0
        self.fulfilled = fulfilled
        self.interactFunc = interactFunc

    # Changes the current interaction level by the given amount, bounding it within range [0, interaction.levels]
    def change_interaction(self, change_amount: int):
        self.currentLevel = max(0, min(self.currentLevel + change_amount, self.levels))

    # Returns the appropriate response to "Interact" command,
    # with required objects taking precedence over interaction level
    # i.e. if a player is on interaction level 1 and also has gathered all required skills, objects, and clues to
    # interact with object, will return the latter interact text
    def get_text(self, player: Player):
        if self.interactFunc is None:  # TODO: Check for held item and see if can be used, if not return text saying so
            player_tools = player.skills + player.clues + ([player.held_item] if player.held_item != [] else [])
            player_tools = list(map(lambda x: x if x is str else x.name, player_tools))
            print(player_tools)

            for items in self.required:
                fulfilled = all(map(lambda x: x in player_tools, items))
                if fulfilled:
                    keyName = " ".join(items)
                    self.fulfilled = True
                    # TODO: Add a check to remove player item if it is used.
                    return self.text[keyName]

            if self.fulfilled:
                return self.text["fulfilled"]
            else:
                self.change_interaction(1)
                return self.text[self.currentLevel]
        else:
            return self.interactFunc(player)
