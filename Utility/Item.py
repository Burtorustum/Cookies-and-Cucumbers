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
    def __init__(self, name, room1: str, room2: str, locked: bool, interactDict={}, requiredItems=[]):
        requiredItems.append(["lockpicking", "pin"])
        interactDict["lockpicking pin"] = "Using your nimble fingers and recently acquired bobby pin, you carefully " \
                                          "pick the door's lock."
        interactDict["fulfilled"] = "You open the unlocked door, and move into the adjacent room."
        door_interact = Interaction(0, interactDict, requiredItems, (not locked), self.interact_function)
        super().__init__(name, [], "You try to wrap your arms around the door to yank it off its hinges,"
                                   " but unsurprisingly, you can't do that. Oh well.", door_interact, False)
        self.room1 = room1
        self.room2 = room2

    def get_examine(self, player: Player):
        if player.cur_room.name == self.room1:
            if self.interact.fulfilled:
                return "The unlocked door leads to the " + self.room2
            else:
                return "The locked door leads to the " + self.room2
        else:
            if self.interact.fulfilled:
                return "The unlocked door leads to the " + self.room1
            else:
                return "The locked door leads to the " + self.room1

    def interact_function(self, player: Player):
        player_tools = player.skills.append(player.clues.append(player.held_item))
        for items in self.interact.required:
            fulfilled = all((lambda x: x in player_tools) for item in items)
            if fulfilled:
                key_name = " ".join(items)
                self.fulfilled = True
                return self.interact.text[key_name]
        else:
            if self.fulfilled: # TODO: Check fulfillment first
                if player.cur_room.name == self.room1:
                    player.cur_room = name_to_room(self.room2)  # TODO: Implement name_to_room
                else:
                    player.cur_room = name_to_room(self.room1)
                return self.interact.text["fulfilled"]
            else:
                return self.interact.text[self.interact.currentLevel]
