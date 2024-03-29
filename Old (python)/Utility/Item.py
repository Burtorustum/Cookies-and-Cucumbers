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

    def __init__(self, name, examine: list, pickup: str, interact: Interaction, holdable: bool, room: str):
        self.name = name
        self.examine = examine
        self.pickup = pickup
        self.interact = interact
        self.holdable = holdable
        self.room = room

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
    defaultDict = {0: "You try to open the door, but it remains firmly locked.\nIf only there was a way to "
                      "unlock it...",
                   "lockpicking pin": "Using your nimble fingers and recently acquired bobby pin, you carefully "
                                      "pick the door's lock",
                   "fulfilled": "You open the unlocked door, and move into the adjacent room."}

    def __init__(self, name, room1: str, room2: str, locked: bool, interact_dict=defaultDict, required_items=[]):
        required_items.append(["lockpicking", "pin"])
        door_interact = Interaction(0, interact_dict, required_items, (not locked), self.interact_function)
        super().__init__(name, [], "You try to wrap your arms around the door to yank it off its hinges,\n"
                                   "but unsurprisingly, you can't do that. Oh well.", door_interact, False, "")
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
        player_tools = player.skills + player.clues + [player.held_item] if player.held_item != [] else []

        if self.interact.fulfilled:
            if player.cur_room.name == self.room1:
                player.cur_room = name_to_room(self.room2)
            else:
                player.cur_room = name_to_room(self.room1)
            return self.interact.text["fulfilled"]

        for items in self.interact.required:
            fulfilled = all(map(lambda x: x in player_tools, items))
            if fulfilled:
                key_name = " ".join(items)
                self.interact.fulfilled = True
                return self.interact.text[key_name]

        return self.interact.text[self.interact.currentLevel]


# TODO: Update with objects for each room
def name_to_room(room: str):
    if room == "Bedroom":
        return bedroom
    if room == "Hallway":
        return hallway
    if room == "Reading Room":
        return None
    if room == "Servant Quarters":
        return None
    if room == "Kitchen":
        return None
    return None


# bad but works...
def parse_text(text: str):
    max_len = 90
    indices = [i for i, x in enumerate(text) if x == " "]
    split_text = text.split(" ")

    for i in range(len(indices)):
        if indices[i] > max_len:
            max_len += 90
            split_text[i] += "\n"

    return ' '.join(split_text)


# ---------------------------------------------------------------------------------------------------------------------
# INSTANTIATIONS:

# INTRO NARRATION

narration_text = [parse_text("\"No cookies!\" hisses your stepmother, Monica. Ear pressed against your bedroom door, "
                             "you’re eavesdropping on your stepmother’s hallway conversation with the butler.\"And "
                             "don’t let "
                             "them "
                             "out of the room! Not if you know what's good for you!\"Monica stomps off and her "
                             "footsteps fade "
                             "down the hallway, and you hear Butler [Eaveswood] give a muffled sigh. Stepmother is "
                             "being mean "
                             "again, you think to yourself, and using the lamplight streaming from under the door to "
                             "guide you, "
                             "you tiptoe back to your bed. No "
                             "cookies? You frown.Then you smile. Yes cookies! :)) ")]

narration_interact_text = {
    0: "A little later, you hear the familiar footsteps of your father approaching your door. The door "
       "eases open,\n"
       "and the silhouette of father comes in, trailed by Butler Eaveswood."
       "Sitting on the side of your bed, \nyour father and Eaveswood pull back the covers for you and you "
       "lie back in a mountain of pillows.\n"
       "\"Goodnight, sleep well,\" says father, eyes crinkling with a smile. The "
       "sliver of light from the hallway\n disappears as the door closes between "
       "the two. You are now alone in bed,\nsurrounded again by darkness and "
       "the crack of orange glow underneath the door.\nNow, about those "
       "cookies..."}


def _narration_interact_func(player: Player):
    player.cur_room = dark_bedroom
    return narration_interact_text[0]


narration_interact = Interaction(0, narration_interact_text, interactFunc=_narration_interact_func)

listen = Item("Put ear to door", narration_text, "What does that even mean?", narration_interact, False, "")

narration_room = Room("Dark Bedroom", [listen], "Someone is talking outside your door...")

# DARK BEDROOM

light_examine = ["It's your bedside lamp."]
light_pickup = "The lamp is attached to the wall, you can't pick it up!"
light_interact_text = {0: "You flip on the lamp, and the room is illuminated.",
                       1: "You flip off the lamp, and the room plunges back into darkness"}


def _lightswitch(player: Player):
    if player.cur_room.name == "Dark Bedroom":
        player.cur_room = bedroom
        return light_interact_text[0]

    player.cur_room = dark_bedroom
    return light_interact_text[1]


light_interact = Interaction(0, light_interact_text, interactFunc=_lightswitch)
light = Item("Lamp", light_examine, light_pickup, light_interact, False, "Dark Bedroom")

dark_bedroom = Room("Dark Bedroom", [light],
                    "A little later, you hear the familiar footsteps of your father approaching your door. The door "
                    "eases open,\n"
                    "and the silhouette of father comes in, trailed by Butler Eaveswood."
                    "Sitting on the side of your bed, \nyour father and Eaveswood pull back the covers for you and you "
                    "lie back in a mountain of pillows.\n"
                    "\"Goodnight, sleep well,\" says father, eyes crinkling with a smile. The "
                    "sliver of light from the hallway\n disappears as the door closes between "
                    "the two. You are now alone in bed,\nsurrounded again by darkness and "
                    "the crack of orange glow underneath the door.\nNow, about those "
                    "cookies...")

# BEDROOM:

bunnyExamine = ["You go over to the bunny and cage and you notice some cucumbers bagged up on the side, \nwith a "
                "paper note "
                "from your nanny reminding you not to eat the cucumbers. \nAs if you would forget that you are "
                "deathly "
                "allergic to cucumbers… You can do with the cucumbers\nwhat you please, although your poor bunny sounds"
                "like he's really hungry."]
bunnyPickup = parse_text("Against all rules of the theory of human interaction with cute fluffy small animals, "
                         "you ignore your starving bunny and pick him up in his cage.")
bunnyInteractText = {0: "You feed the bunny a bit of cucumber. It seems a bit happier."}
# TODO: Make it so the bunny has levels of happiness (interact levels)
bunnyInteraction = Interaction(0, bunnyInteractText)
bunny = Item("Bunny", bunnyExamine, bunnyPickup, bunnyInteraction, True, "Bedroom")

booksExamine = ["There are three books on your bookshelf. Your stepmother took away all your others when\n"
                "she caught you reading them late at night, so there's not much left now. \nHansel and Gretel: Man,"
                "you really want some cookies\nA heavily abridged encyclopedia: You definitely haven't fed your "
                "bunny some of the pages\nWheelock's Latin: A book in some foreign language by someone named R. S. "
                "Enic. "
                "What a weird name."]
booksPickup = "You grab the three books from the bookshelf."
bookInteractText = {0: "You are so desperate to take your mind off of cookies that you start reading the "
                       "encyclopedia,\n "
                       "but quickly realize your mistake. Who wants to read that?",
                    1: "Reading the books didn't distract you from the thought of cookies before, but maybe you can "
                       "try again...\nNope, still didn't work."}
bookInteraction = Interaction(1, bookInteractText)
books = Item("Books", booksExamine, booksPickup, bookInteraction, True, "Bedroom")

globeExamine = ["Your real mother gave this globe to you as a birthday present just a few weeks before she died. \nOn "
                "it, "
                " you can still see the faded circles on the places you and her and father planned\nto visit on your "
                "trip around the world."]
globePickup = "You pick up the globe rather awkwardly."
globeInteractText = {0: "You spin the globe absent-mindedly. Nothing happens."}
globeInteraction = Interaction(0, globeInteractText)
globe = Item("Globe", globeExamine, globePickup, globeInteraction, True, "Bedroom")

rockingHorseExamine = ["You always wanted a real horse, but father always said that you couldn't take care of one.\n"
                       "Instead he got you this rocking horse. It's too small for you now."]
rockingHorsePickup = "You struggle to lift up the wooden horse, but you eventually get a good grip."
rockingHorseInteractText = {0: "You try to sit on the rocking horse, but it's much too small for you, \nand you quickly"
                               " get off for fear of breaking it."}
rockingHorseInteraction = Interaction(0, rockingHorseInteractText)
rockingHorse = Item("Rocking horse", rockingHorseExamine, rockingHorsePickup, rockingHorseInteraction, True, "Bedroom")

# window = Item("Window", window_examine, window_pickup, window_interact, False)

# TODO: Change to be unlocked, then locked after exiting first time, w dialogue (item instead of door)
bedroom_door = Door("Bedroom door", "Bedroom", "Hallway", True)

window_examine = ["You stare wistfully at the totally normal and ordinary window. Why? Who knows."]
window_pickup = "You try to carry a window attached to the wall... Unsurprisingly, you fail."
window_interact_text = {
    0: parse_text(
        "As you lean in towards the window, you can almost smell a batch of cookies wafting up from below. Yep, "
        "definitely cookies. Who could be making cookies this late? Doesn’t matter. Maybe you can get some! You "
        "can’t lean out too far though, because the window can’t hold itself up, and you’re not really in the mood for "
        "death by window guillotine. Yo do notice, however, a small ledge right under the window..."),
    "Rocking horse": "You successfully prop open the window with the rocking horse.",
    "fulfilled": "You hop out the window onto the ledge, and carefully make your way to the adjacent window. You "
                 "enter the Reading Room. "}

# TODO: Give this an actual interact func so that u can travel out the window (connect to event for pick up gold guy)
window_interact = Interaction(0, window_interact_text, required=[[rockingHorse.name]])

window = Item("Window", window_examine, window_pickup, window_interact, False, "Bedroom")

bedroom = Room("Bedroom", [light, bunny, books, globe, rockingHorse, bedroom_door, window], "You are in your own "
                                                                                            "bedroom.")

# HALLWAY:

hallway = Room("Hallway", [bedroom_door], "This hallway connects every room in the house. How convenient!")

# READING ROOM:


# KITCHEN:


# HALLWAY:


# SERVANT'S QUARTERS:
