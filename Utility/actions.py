from Utility.Player import Player
from Utility.Room import Room
from Utility.Item import Item


def move(room: Room):
    print(room.name)


def examine(item: Item):
    return item.examine_text


def interact(player: Player, item: Item):
    print(item.name, player.clues)


def pick_up(player: Player, item: Item):
    if item.holdable and not player.is_holding_obj():
        player.held_obj = item
        return item.pickup_text
    elif not item.holdable:
        return item.pickup_text
    else:
        return "You are already holding something!"


def drop(player: Player):
    if player.is_holding_obj():
        text = "Dropped the " + player.held_item.name + "."
        player.held_item = None
        return text

    return "Nothing to drop!"
