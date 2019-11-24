from .Interactions import *
from .Room import *
from .Player import *


class Item:
    """
    An Item represents an object in the game with associated actions, where:
        - examine represents a list of "Examine" command responses. If object is changeable (i.e. Interaction can be
            fulfilled), first element is unfulfilled and second is fulfilled; else, first element is default
        - pickup is the "Pick Up" response
        - interact is the Interaction object for the item
        - holdable represents whether or not the object can be held
    """

    def __init__(self, name, examine: list, pickup: str, interact: Interaction, holdable: bool):
        self.name = name
        self.examine = examine
        self.pickup = pickup
        self.interact = interact
        self.holdable = holdable

    # Returns appropriate "Examine" command text
    # and yes the player parameter is useless but I'm tired and I want the override below to work so oh well.
    def get_examine(self, player: Player):
        if self.interact.fulfilled is False:
            return self.examine[1]
        else:
            return self.examine[0]

    def get_pickup(self, player: Player):
        return self.pickup


class Door(Item):

    def __init__(self, name, room1: Room, room2: Room, locked: bool, interactDict={}, requiredItems=[]):
        interactRequire = requiredItems.append(["lockpicking", "pin"])
        interactDict["lockpicking pin"] = "Using your nimble fingers and recently acquired bobby pin, you carefully " \
                                          "pick the door's lock."
        interactDict["fulfilled"] = "You open the unlocked door, and move into the adjacent room."
        doorInteract = Interaction(0, interactDict, interactRequire, (not locked), self.interactFunction)
        super().__init__(name, [], "You try to wrap your arms around the door to yank it off its hinges,"
                                   " but unsurprisingly, you can't do that. Oh well.", doorInteract, False)
        self.room1 = room1
        self.room2 = room2

    def get_examine(self, player: Player):
        if player.cur_room == self.room1:
            if self.interact.fulfilled:
                return "The unlocked door leads to the " + self.room2.name
            else:
                return "The locked door leads to the " + self.room2.name
        else:
            if self.interact.fulfilled:
                return "The unlocked door leads to the " + self.room1.name
            else:
                return "The locked door leads to the " + self.room1.name

    def interactFunction(self, player: Player):
        playerTools = player.skills.append(player.clues.append(player.held_obj))
        for items in self.interact.required:
            fulfilled = all((lambda x: x in playerTools) for item in items)
            if fulfilled:
                keyName = "".join(items)
                self.fulfilled = True
                return self.interact.text[keyName]
        else:
            if self.fulfilled:
                if player.cur_room == self.room1:
                    player.cur_room = self.room2
                else:
                    player.cur_room = self.room1
                return self.interact.text["fulfilled"]
            else:
                return self.interact.text[self.interact.currentLevel]
