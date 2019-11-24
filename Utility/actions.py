from .Player import *
from .Room import *
from .Item import *

def move(room: Room):
    return "You are now in the " + room.name


def examine(item: Item):
    return item.get_examine()


def interact(player: Player, item: Item):
    return item.interact.getText(player)


def pick_up(player: Player, item: Item):
    if item.holdable and player.held_obj is None:
        player.held_obj = item
        return item.pickup
    elif not item.holdable:
        return item.pickup
    else:
        return "You're already carrying " + player.held_obj.name + \
               ", and though you are self-assured in your extremely large arms for a child," \
               " you can't quite carry both objects. You should really work on growing. Or maybe just drop what you're" \
               "holding."


def drop(player: Player, currentRoom: Room):
    held_obj = player.held_obj
    if held_obj is not None:
        currentRoom.objects.append(held_obj)
        player.held_obj = None
        return "You dropped the " + held_obj
    else:
        return "You fling your arms open wide as if you were dropping something, only you weren't holding anything."
