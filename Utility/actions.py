from .Player import *
from .Room import *
from .Item import *


def move(room: Room):
    return "You are now in the " + room.name


def examine(item: Item):
    return item.get_examine


def interact(player: Player, item: Item):
    return item.interact.get_text(player)


def pick_up(player: Player, item: Item):
    if item.holdable and player.held_item is None:
        player.held_item = item
        player.cur_room.objects.remove(item)
        return item.get_pickup(player)
    elif not item.holdable:
        return item.get_pickup(player)
    else:
        return "You're already carrying " + player.held_item.name + \
               ", and though you are self-assured in your extremely large arms for a child," \
               " you can't quite carry both objects. You should really work on growing. Or maybe just drop what you're" \
               "holding."


def drop(player: Player):
    held_item = player.held_item
    if held_item is not None:
        player.cur_room.objects.append(held_item)
        player.held_item = None
        return "You dropped the " + held_item.name
    else:
        return "You fling your arms open wide as if you were dropping something, only you weren't holding anything."
