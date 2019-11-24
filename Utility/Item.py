from Utility.Room import Room
from .Interactions import *
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
    def __init__(self, name, room1: str, room2: str, locked: bool, interact_dict={}, required_items=[]):
        required_items.append(["lockpicking", "pin"])
        interact_dict["lockpicking pin"] = "Using your nimble fingers and recently acquired bobby pin, you carefully " \
                                           "pick the door's lock."
        interact_dict["fulfilled"] = "You open the unlocked door, and move into the adjacent room."
        door_interact = Interaction(0, interact_dict, required_items, (not locked), self.interact_function)
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
        player_tools = player.skills + (player.clues + player.held_item)  # Previously:
        #  player_tools = player.skills.append(player.clues.append(player.held_item))
        # however, this would return None and modify the player skills permanently, increasing size forever
        for items in self.interact.required:
            fulfilled = all((lambda x: x in player_tools) for item in items)
            if fulfilled:
                key_name = " ".join(items)
                self.fulfilled = True
                return self.interact.text[key_name]
        else:
            if self.fulfilled:  # TODO: Check fulfillment first
                if player.cur_room.name == self.room1:
                    player.cur_room = name_to_room(self.room2)
                else:
                    player.cur_room = name_to_room(self.room1)
                return self.interact.text["fulfilled"]
            else:
                return self.interact.text[self.interact.currentLevel]


def name_to_room(room: str):
    if room == "bedroom":
        return bedroom
    if room == "hallway":
        return None
    if room == "reading room":
        return None
    if room == "servant quarters":
        return None
    if room == "kitchen":
        return None
    return None


bunnyExamine = ["You go over to the bunny and cage and you notice some cucumbers bagged up on the side, with a "
                "paper note "
                "from your nanny reminding you not to eat the cucumbers. As if you would forget that you were deathly "
                "allergic to cucumbers… You can do with the cucumbers what you please, although your poor bunny sounds "
                "like he's really hungry."]
bunnyPickup = "Against all rules of the theory of human interaction with cute fluffy small animals, " \
              "you ignore your starving bunny and pick him up in his cage."
bunnyInteractText = {0: "You do something to interact with the bunny"}
bunnyInteraction = Interaction(0, bunnyInteractText)
bunny = Item("bunny", bunnyExamine, bunnyPickup, bunnyInteraction, True)

booksExamine = ["There are three books on your bookshelf. Your stepmother took away all your others when"
                "she caught you reading them late at night, so there's not much left now. \nHansel and Gretel: Man,"
                "you really want some cookies\nA heavily abridged encyclopedia: You definitely haven't fed your "
                "bunny some of the pages\nWheelock's Latin: A book in some foreign language by someone named R. S. Enic."
                "What a weird name."]
booksPickup = "You grab the three books from the bookshelf."
bookInteractText = {0: "You are so desperate to take your mind off of cookies that you start reading the encyclopedia, "
                       "but quickly realize your mistake. Who wants to read that?",
                    1: "Reading the books didn't distract you from the thought of cookies before, but maybe you can "
                       "try again... Nope, still didn't work."}
bookInteraction = Interaction(1, bookInteractText)
books = Item("books", booksExamine, booksPickup, bookInteraction, True)

globeExamine = ["Your real mother gave this globe to you as a birthday present just a few weeks before she died. On it,"
                " you can still see the faded circles on the places you and her and father planned to visit on your "
                "trip around the world."]
globePickup = "You pick up the globe rather awkwardly."
globeInteractText = {0: "You spin the globe absent-mindedly. Nothing happens."}
globeInteraction = Interaction(0, globeInteractText)
globe = Item("globe", globeExamine, globePickup, globeInteraction, True)

rockingHorseExamine = ["You always wanted a real horse, but father always said that you couldn't take care of one."
                       "Instead he got you this rocking horse. It's too small for you now."]
rockingHorsePickup = "You struggle to lift up the wooden horse, but you eventually get a good grip."
rockingHorseInteractText = {0: "You try to sit on the rocking horse, but it's much too small for you, and you quickly"
                               "get off for fear of breaking it."}
rockingHorseInteraction = Interaction(0, rockingHorseInteractText)
rockingHorse = Item("rocking horse", rockingHorseExamine, rockingHorsePickup, rockingHorseInteraction, True)

door = Door("door", "bedroom", "hallway", False)

bedroom = Room("Bedroom", [bunny, books, globe, rockingHorse, door], "You are in your own bedroom.", [])
